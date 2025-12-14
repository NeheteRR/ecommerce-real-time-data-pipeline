from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017")
db = client["ecommerce_db"]
collection = db["products"]

# Create
@app.route("/products", methods=["POST"])
def create_product():
    data = request.json
    collection.insert_one(data)
    return jsonify({"msg": "Product added"}), 201

# Read
@app.route("/products", methods=["GET"])
def get_products():
    products = list(collection.find({}, {"_id": 0}))
    return jsonify(products)

# Update
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    updates = request.json
    collection.update_one({"id": product_id}, {"$set": updates})
    return jsonify({"msg": "Product updated"})

# Delete
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    collection.delete_one({"id": product_id})
    return jsonify({"msg": "Product deleted"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
