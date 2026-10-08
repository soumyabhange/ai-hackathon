from fastapi import FastAPI

app = FastAPI()

@app.get("/products")
def get_products():
    return {
        "products": [
            {"id": 1, "name": "Laptop"},
            {"id": 2, "name": "Phone"}
        ]
    }

@app.post("/products")
def create_product(name: str, price: float):
    return {
        "message": f"Product {name} created",
        "price": price
    }