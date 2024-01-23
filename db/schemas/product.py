def product_schema(product) -> dict:
    return {"id": str(product["_id"]),
            "name": product["name"],
            "description": product["description"]}
    
def products_schema(products) -> list:
    return [product_schema(product) for product in products]