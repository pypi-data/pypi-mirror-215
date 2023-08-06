from setuptools import setup, find_packages

VERSION = '0.0.5' 
DESCRIPTION = 'Spark MinIO Handler Package'
LONG_DESCRIPTION = 'Pacote para gerenciar views e dataframes spark consumindo de tabelas JSON armazenadas no Object Storage MinIO'

# Setting up
setup(
       # 'name' deve corresponder ao nome da pasta 'verysimplemodule'
        name="SparkMinIOHandle", 
        version=VERSION,
        author="Yuri Dimitri",
        author_email="yuridrcosta@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # adicione outros pacotes que 
        # precisem ser instalados com o seu pacote. Ex: 'caer'
        
        keywords=['python', 'minio', 'spark'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)