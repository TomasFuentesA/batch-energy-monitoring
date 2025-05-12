from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import *
import time
import os

# Crear SparkSession
spark = SparkSession.builder \
    .appName("InsertCleanDataToPostgres") \
    .getOrCreate()

# Configurar conexión JDBC
jdbc_url = "jdbc:postgresql://postgres:5432/batch_energy_monitoring"  # Cambia si tu BD se llama distinto
db_properties = {
    "user": "energyuser",
    "password": "energypass",
    "driver": "org.postgresql.Driver"
}

# Ruta a los datos limpios
raw_data_path = "/app/data/raw"

consumption_schema = StructType([StructField('timestamp', TimestampType(), True),
                                 StructField('house_id', StringType(), True),
                                 StructField('consumption_kWh', FloatType(), True),
                                 StructField('temperature', FloatType(), True),
                                 StructField('voltage', FloatType(), True)])

# Leer archivos CSV de la carpeta de datos limpios
def process_raw_data():
    if not os.path.exists(raw_data_path):
        print("Clean data folder not found.")
        return

    # Leer todos los archivos CSV en el directorio
    df_clean = spark.read.format("csv") \
        .option("header", True) \
        .schema(consumption_schema) \
        .load(f"{raw_data_path}/*.csv")

    if df_clean.rdd.isEmpty():
        print("No hay datos nuevos para insertar.")
        return

    # Insertar en la tabla PostgreSQL
    df_clean.write.jdbc(
        url=jdbc_url,
        table="energy_data_raw",
        mode="append",
        properties=db_properties
    )

    print(f"Datos insertados correctamente: {df_clean}")

    for filename in os.listdir(raw_data_path):
        if filename.endswith(".csv"):
            os.remove(os.path.join(raw_data_path, filename))

    

# Ejecutar el proceso una vez o en bucle si prefieres
if __name__ == "__main__":
    while True:
        try:
            process_raw_data()
            time.sleep(10)  # Espera 10 segundos antes de revisar de nuevo
        except Exception as e:
            print(f"Error al insertar datos: {e}")
            time.sleep(10)