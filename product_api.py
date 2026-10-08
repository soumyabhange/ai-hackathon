from flask import Flask, request
app = Flask(__name__)
@app.route("/products", methods=["GET"])
def get_products():
    return {"products": []}
@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    return {
        "id": product_id,
        "name": "Laptop",
        "price": 50000
    }
@app.route("/products", methods=["POST"])
def create_product():
    data = request.json
    return {
        "message": "Product created",
        "product": data
    }
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    return {
        "message": "Product deleted"
    }
if __name__ == "__main__":
    app.run(debug=True)