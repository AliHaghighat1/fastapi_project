from fastapi import APIRouter

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("/")
def get_products():
    return {
        "products": [
            {"id": 1, "name": "Laptop"},
            {"id": 2, "name": "Phone"}
        ]
    }

@router.get("/{product_id}")
def get_product(product_id: int):
    return {
        "id": product_id,
        "name": f"Product {product_id}"
    }