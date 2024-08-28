from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace, to_timestamp
import os

READ_PATH = os.getenv('AUDIT_PATH')
# READ_PATH = os.getenv('AUDIT_PATH')/f'messages_audit'
WRITE_PATH = os.getenv('AUDIT_PATH')
WRITE_PATH = f"{WRITE_PATH}/messages_processed"

spark = SparkSession.builder.appName("KafkaProcess").getOrCreate()

df = spark.read.json(READ_PATH)
df = df.filter(col("sender") != "[INFO]")
# df = df.filter(col("end") != True)
# df = df.withColumn("message", regexp_replace(col("message"), r"\n", " "))
# df = df.withColumn("timestamp", to_timestamp("timestamp", "yyyy-MM-dd'T'HH:mm:ss.SSSSSS"))
# df.write.mode("overwrite").parquet(WRITE_PATH)

print(WRITE_PATH)
spark.stop()
