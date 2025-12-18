from flask import Flask, request, jsonify, render_template, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# MongoDB
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
        p["_id"] = str(p["_id"])
        products.append(p)
    return jsonify(products)


@app.route("/products/<string:product_id>", methods=["GET"])
def get_product_by_id(product_id):
    try:
        product = collection.find_one({"_id": ObjectId(product_id)})
    except:
        return {"error": "Invalid product ID"}, 400

    if not product:
        return {"error": "Product not found"}, 404

    product["_id"] = str(product["_id"])
    return jsonify(product)


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


@app.route("/products/<string:product_id>", methods=["DELETE"])
def delete_product(product_id):
    collection.delete_one({"_id": ObjectId(product_id)})
    return jsonify({"msg": "Product deleted"})


@app.route("/")
def ui_home():
    products = list(collection.find())
    for p in products:
        p["_id"] = str(p["_id"])
    return render_template("index.html", products=products)


@app.route("/add", methods=["GET", "POST"])
def ui_add_product():
    if request.method == "POST":
        data = {
            "title": request.form["title"],
            "price": float(request.form["price"]),
            "category": request.form["category"]
        }
        collection.insert_one(data)
        return redirect(url_for("ui_home"))
    return render_template("add.html")


@app.route("/edit/<id>", methods=["GET", "POST"])
def ui_edit_product(id):
    product = collection.find_one({"_id": ObjectId(id)})

    if request.method == "POST":
        collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "title": request.form["title"],
                "price": float(request.form["price"]),
                "category": request.form["category"]
            }}
        )
        return redirect(url_for("ui_home"))

    product["_id"] = str(product["_id"])
    return render_template("edit.html", product=product)


@app.route("/delete/<id>")
def ui_delete_product(id):
    collection.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("ui_home"))


if __name__ == "__main__":
    app.run(debug=False)
