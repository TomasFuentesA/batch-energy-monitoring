from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import os

current_path = os.getcwd()

spark = SparkSession \
    .builder \
    .appName("readEnergyConsumption") \
    .master("local[4]")\
    .getOrCreate()


consumption_schema = StructType([StructField('timestamp', TimestampType(), True),
                                 StructField('house_id', StringType(), True),
                                 StructField('consumption_kWh', FloatType(), True),
                                 StructField('temperature', FloatType(), True),
                                 StructField('voltage', FloatType(), True)])



try:
    consumption_customer = spark.readStream.format("csv").schema(consumption_schema)\
                    .option("header", True).option("maxFilesPerTrigger",1)\
                    .load(f"{current_path}/data/raw")


    df_clean = consumption_customer.dropna()
    df_clean = df_clean.filter((df_clean['consumption_kWh'] > 0) & (df_clean['consumption_kWh'] != 9999))
    df_clean = df_clean.filter((df_clean['voltage'] != 9999) & (df_clean['voltage'] != -9999))
    df_clean = df_clean.filter((df_clean['temperature'] != 9999) & (df_clean['temperature'] != -9999))
    #df_after_clean = df_clean.writeStream.format("console").outputMode("append").option("truncate", False).start()
    df_after_clean = df_clean.writeStream.format("csv").outputMode("append").option("path", f"{current_path}/data/clean").option("checkpointLocation", f"{current_path}/data/clean/checkpoint").start().awaitTermination()
    
except Exception as e:
    print(f"An error occurred: {e}")
