from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# FIXED Mongo URI
client = MongoClient("mongodb://localhost:27018")
db = client["ecommerce_db"]
collection = db["products"]

@app.route("/products", methods=["POST"])
def create_product():
    data = request.json
    result = collection.insert_one(data)
    return jsonify({
        "msg": "Product added",
        "id": str(result.inserted_id)
    }), 201

@app.route("/products", methods=["GET"])
def get_products():
    products = []
    for p in collection.find():
        p["_id"] = str(p["_id"])  # convert ObjectId to string
        products.append(p)
    return jsonify(products)

@app.route("/products/<string:product_id>", methods=["PUT"])
def update_product(product_id):
    updates = request.json

    result = collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": updates}
    )

    if result.matched_count == 0:
        return {"error": "Product not found"}, 404

    return {"message": "Product updated successfully"}

@app.route("/products/<string:product_id>", methods=["GET"])
def get_product_by_id(product_id):
    try:
        product = collection.find_one({"_id": ObjectId(product_id)})
    except:
        return {"error": "Invalid product ID format"}, 400

    if not product:
        return {"error": "Product not found"}, 404

    product["_id"] = str(product["_id"])
    return jsonify(product)


@app.route("/")
def home():
    return {"message": "E-commerce API is running"}


@app.route("/products/<string:product_id>", methods=["DELETE"])
def delete_product(product_id):
    collection.delete_one(
        {"_id": ObjectId(product_id)}
    )
    return jsonify({"msg": "Product deleted"})


if __name__ == "__main__":
    app.run(debug=False)
