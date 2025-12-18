from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

# Kafka + Mongo config
KAFKA_BROKER = "ec_kafka:9092"   # ✅ Windows → Docker Kafka
KAFKA_TOPIC = "products_raw"
MONGO_URI = "mongodb://host.docker.internal:27018"
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

# Spark session
spark = SparkSession.builder \
    .appName("KafkaSparkMongoPipeline") \
    .config("spark.mongodb.connection.uri", MONGO_URI) \
    .config("spark.hadoop.io.native.lib.available", "false") \
    .getOrCreate()


# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "earliest") \
    .load()

# Kafka value → JSON → columns
products_df = df.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), product_schema).alias("data")) \
    .select("data.*")

# Transformation
products_transformed = products_df.withColumn(
    "discounted_price",
    col("price") * 0.9
)

# Write to MongoDB
query = products_transformed.writeStream \
    .format("mongodb") \
    .option("spark.mongodb.database", MONGO_DB) \
    .option("spark.mongodb.collection", MONGO_COLLECTION) \
    .option("checkpointLocation", "/tmp/spark_checkpoints/products") \
    .outputMode("append") \
    .start()

query.awaitTermination()
