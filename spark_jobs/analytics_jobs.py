from pyspark.sql import SparkSession

MONGO_URI = "mongodb://localhost:27017"
MONGO_DB = "ecommerce_db"
MONGO_COLLECTION = "products"

spark = SparkSession.builder \
    .appName("EcommerceAnalytics") \
    .config("spark.mongodb.read.connection.uri", MONGO_URI) \
    .config("spark.mongodb.read.database", MONGO_DB) \
    .config("spark.mongodb.read.collection", MONGO_COLLECTION) \
    .getOrCreate()

# Load data
df = spark.read.format("mongodb").load()

# Example analytics
df.groupBy("category").avg("price").show()
df.orderBy(df.price.desc()).show(5)
df.groupBy("category").count().orderBy("count", ascending=False).show()
