# chat_analyzer.py

import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col, regexp_replace, hour

# 명령줄 인수 처리
if len(sys.argv) != 2:
    print("Usage: chat_analyzer.py <choice>")
    sys.exit(-1)

choice = sys.argv[1]

# Spark 세션 생성
spark = SparkSession.builder.appName("ChatAnalyzer").getOrCreate()

# JSON 파일 로드
df = spark.read.json("/home/kyuseok00/teamproj/chat/data/messages.json")
df = df.filter(col("sender") != "[INFO]")
df = df.withColumn("message", regexp_replace(col("message"), r"\n", " "))

if choice == '1':
    # User-wise message count
    user_count = df.groupBy("sender").count()
    user_count.show()

elif choice == '2':
    # Word frequency analysis
    df_words = df.withColumn("word", explode(split(col("message"), " ")))
    df_words = df_words.filter(col("word") != "")
    word_count = df_words.groupBy("word").count().orderBy(col("count").desc())
    word_count.show()

elif choice == '3':
    # Hourly message count
    from pyspark.sql.functions import hour, minute, col
    df_with_time = df.withColumn("hour", hour(col("timestamp"))).withColumn("minute", minute(col("timestamp")))
    time_count = df_with_time.groupBy("hour", "minute").count().orderBy("hour", "minute")
    # z.show(time_count)
    time_count.show()

else:
    print("Invalid choice. Please enter 1, 2, or 3.")

# Spark 세션 종료
spark.stop()

