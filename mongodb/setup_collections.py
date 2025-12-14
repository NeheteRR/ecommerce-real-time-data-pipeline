from pymongo import MongoClient

# MongoDB connection
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "ecommerce_db"
COLLECTION_NAME = "products"

def setup_mongodb():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    # Drop old collection (optional - for clean setup)
    if COLLECTION_NAME in db.list_collection_names():
        db.drop_collection(COLLECTION_NAME)

    # Create new collection
    collection = db[COLLECTION_NAME]

    # Example: Create unique index on product "id"
    collection.create_index("id", unique=True)

    # Example: Create index on category for faster queries
    collection.create_index("category")

    print(f"MongoDB setup complete. Database: {DB_NAME}, Collection: {COLLECTION_NAME}")

if __name__ == "__main__":
    setup_mongodb()
