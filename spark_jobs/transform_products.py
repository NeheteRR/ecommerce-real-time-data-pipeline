from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

# Kafka + Mongo config
KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "products_raw"
MONGO_URI = "mongodb://localhost:27017"
MONGO_DB = "ecommerce_db"
MONGO_COLLECTION = "products"

# Define schema for product JSON
product_schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("title", StringType(), True),
    StructField("price", DoubleType(), True),
    StructField("category", StringType(), True),
    StructField("description", StringType(), True),
    StructField("image", StringType(), True)
])

# Spark session with Mongo connector
spark = SparkSession.builder \
    .appName("KafkaSparkMongoPipeline") \
    .config("spark.mongodb.write.connection.uri", MONGO_URI) \
    .config("spark.mongodb.write.database", MONGO_DB) \
    .config("spark.mongodb.write.collection", MONGO_COLLECTION) \
    .getOrCreate()

# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("subscribe", KAFKA_TOPIC) \
    .load()

# Convert Kafka value (binary) → JSON → DataFrame
products_df = df.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), product_schema).alias("data")) \
    .select("data.*")

# Example transformation: add discounted price column
products_transformed = products_df.withColumn("discounted_price", col("price") * 0.9)

# Write to MongoDB
query = products_transformed.writeStream \
    .format("mongodb") \
    .option("checkpointLocation", "/tmp/spark_checkpoints/products") \
    .outputMode("append") \
    .start()

query.awaitTermination()
