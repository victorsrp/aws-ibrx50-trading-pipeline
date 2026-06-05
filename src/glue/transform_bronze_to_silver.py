import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date
from pyspark.sql.types import DecimalType, LongType

def processar_bronze_para_silver():
    print("Iniciando Spark Session Local com suporte a Apache Iceberg...")
    
    # Inicializa o Spark injetando as bibliotecas do conector do Apache Iceberg
    spark = SparkSession.builder \
        .appName("BronzeToSilverIceberg") \
        .config("spark.jars.packages", "org.apache.iceberg:iceberg-spark-runtime-3.4_2.12:1.3.1") \
        .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
        .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog") \
        .config("spark.sql.catalog.local.type", "hadoop") \
        .config("spark.sql.catalog.local.warehouse", "./warehouse") \
        .getOrCreate()

    # Como você já fez o download dos dados brutos, o Spark vai ler a pasta local
    pasta_bronze = "./bronze/"
    if not os.path.exists(pasta_bronze):
        print("erro: A pasta './bronze/' não foi encontrada. Certifique-se de que o script de ingestão rodou.")
        return

    print("Lendo múltiplos arquivos JSON da Camada Bronze...")
    # O Spark tem o poder de ler todos os subdiretórios de uma vez só usando o caractere curinga *
    df_bruto = spark.read.json("bronze/*/*.json")

    print("Padronizando tipos de dados (Casting) e limpando duplicatas...")
    # Realiza o cast (conversão) dos dados brutos para os tipos financeiros ideais
    df_limpo = df_bruto.select(
        col("Ticker").alias("ticker"),
        to_date(col("Date")).alias("data"),
        col("Open").cast(DecimalType(10, 2)).alias("abertura"),
        col("High").cast(DecimalType(10, 2)).alias("maxima"),
        col("Low").cast(DecimalType(10, 2)).alias("minima"),
        col("Close").cast(DecimalType(10, 2)).alias("fechamento"),
        col("Volume").cast(LongType()).alias("volume")
    ).dropDuplicates(["ticker", "data"]) # Garante a integridade da série temporal

    print("Gravando dados na tabela Apache Iceberg (Camada Silver)...")
    # Escreve os dados estruturando o catálogo local (Hadoop warehouse)
    df_limpo.write \
        .format("iceberg") \
        .mode("overwrite") \
        .save("local.db_trading_larry_williams.tb_silver_historico")

    print("camada Silver criada com sucesso no formato Apache Iceberg!")
    spark.stop()

if __name__ == "__main__":
    processar_bronze_para_silver()