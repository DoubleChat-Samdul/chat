# chat_analyzer.py

import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col, regexp_replace, hour
import matplotlib.pyplot as plt
from wordcloud import WordCloud

if len(sys.argv) != 2:
    print("Usage: chat_analyzer.py <choice>")
    sys.exit(-1)

choice = sys.argv[1]

spark = SparkSession.builder.appName("ChatAnalyzer").getOrCreate()

df = spark.read.json("/home/kyuseok00/teamproj/chat/data/messages.json")
df = df.filter(col("sender") != "[INFO]")
df = df.withColumn("message", regexp_replace(col("message"), r"\n", " "))
df = df.filter(col("end") == False)

if choice == 'user':
    user_count = df.groupBy("sender").count()
    user_count.show()

elif choice == 'word':
    df_words = df.withColumn("word", explode(split(col("message"), " ")))
    df_words = df_words.filter(col("word") != "")
    word_count = df_words.groupBy("word").count().orderBy(col("count").desc()).limit(20)
    word_count_pd = word_count.toPandas() 
    """
    plt.figure(figsize=(10, 6))
    plt.bar(word_count_pd['word'], word_count_pd['count'], color='lightgreen')
    plt.xlabel('Word')
    plt.ylabel('Frequency')
    plt.title('Word Frequency')
    plt.xticks(rotation=45)
    plt.show()
    """
    # WordCloud 시각화
    word_freq = dict(zip(word_count_pd['word'], word_count_pd['count']))
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(word_freq)

    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title('Word Frequency WordCloud')
    plt.show()
    
elif choice == 'time':
    from pyspark.sql.functions import hour, minute, col
    df_with_time = df.withColumn("hour", hour(col("timestamp"))).withColumn("minute", minute(col("timestamp")))
    time_count = df_with_time.groupBy("hour", "minute").count().orderBy("hour", "minute")
    time_count.show()

else:
    print()
    print("********** Invalid choice. Please enter 'user', 'word', or 'time' **********")
    print()

spark.stop()

