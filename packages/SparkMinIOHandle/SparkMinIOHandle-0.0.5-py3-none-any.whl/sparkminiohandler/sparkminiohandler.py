from datetime import datetime

class SparkMinIOHandler:

    def __init__(self, client_minio, bucket_name, spark_session, spark_context):
        self.client_minio = client_minio
        self.bucket_name = bucket_name
        self.spark_session = spark_session
        self.spark_context = spark_context 


    def get_recent_table(self, tablename: str):
        # Padrão de nome dos arquivos
        
        # Obter lista de arquivos correspondentes ao padrão
        arquivos =  [object.object_name for object in self.client_minio.list_objects(self.bucket_name) if f'{tablename}_' in object.object_name]
        
        # Função para extrair a data do nome do arquivo
        def extrair_data(nome_arquivo):
            # O formato do nome do arquivo é NOME_YYYY-MM-DD.json
            data_str = nome_arquivo.split('_')[1].split('.')[0]
            data = datetime.strptime(data_str, '%Y-%m-%d')
            return data
        
        # Ordenar a lista de arquivos pela data mais recente
        arquivos_ordenados = sorted(arquivos, key=lambda x: extrair_data(x), reverse=True)
        
        # Obter o arquivo mais recente
        arquivo_recente = arquivos_ordenados[0]
        print(f"Arquivo mais recente: {arquivo_recente}")
        return arquivo_recente
    
    def load_json_spark_dataframe(self,  filename: str):
        response = self.client_minio.get_object(self.bucket_name, filename)
        with open("temptable.json",'wb') as f:
            f.write(response.data)
        df = self.spark_session.read.option("multiline", "true").json('temptable.json')
        return df
    
    def create_view_from_json_minio(self, tablename) :
        filename = self.get_recent_table(tablename)
        df = self.load_json_spark_dataframe(filename)
        df.createOrReplaceTempView(tablename)
        return True
    
    def create_multiple_table_views(self, tablenames: list):
        for table in tablenames:
            self.create_view_from_json_minio(table) 