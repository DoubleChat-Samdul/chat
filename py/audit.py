from kafka import KafkaConsumer, TopicPartition
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, BooleanType, TimestampType
from json import loads
import os

OFFSET_FILE = '/home/kyuseok00/teamproj/chat/offset.txt'

spark = SparkSession.builder.appName("KafkaAudit").getOrCreate()

def save_offset(offset):
    with open(OFFSET_FILE, 'w') as f:
        f.write(str(offset))

def read_offset():
    if os.path.exists(OFFSET_FILE):
        with open(OFFSET_FILE, 'r') as f:
            return int(f.read().strip())
    return None

def fetch_data():
    output_path = '/home/kyuseok00/teamproj/chat/data/messages_audit'
    
    saved_offset = read_offset()

    consumer = KafkaConsumer(
        bootstrap_servers=['ec2-43-203-210-250.ap-northeast-2.compute.amazonaws.com:9092'],
        value_deserializer=lambda x: loads(x.decode('utf-8')),
        group_id="chat_team2",
        enable_auto_commit=False,
        consumer_timeout_ms=5000
    )

    p = TopicPartition('team2', 0)
    consumer.assign([p])

    if saved_offset is not None:
        consumer.seek(p, saved_offset)
    else:
        consumer.seek_to_beginning(p)

    message_list = []

    for message in consumer:
        data = message.value
        message_list.append(data)

        save_offset(message.offset + 1)

    schema = StructType([
        StructField("sender", StringType(), True),
        StructField("message", StringType(), True),
        StructField("end", BooleanType(), True),
        StructField("timestamp", StringType(), True)
    ])

    if message_list:
        df = spark.createDataFrame(message_list, schema)
        df.write.mode("append").parquet(output_path)

    consumer.close()

fetch_data()

spark.stop()
