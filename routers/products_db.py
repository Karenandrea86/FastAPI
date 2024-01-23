# Products DB API

from fastapi import APIRouter, HTTPException, status
from db.models.product import Product
from db.schemas.product import product_schema, products_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/productdb",
                   tags=["productdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

@router.get("/", response_model=list[Product])
async def products():
    return products_schema(db_client.products.find())

# Path
@router.get("/{id}")
async def product(id: str):
    return search_product("_id", ObjectId(id))

# Query
@router.get("/")
async def product():
    return search_product("_id", ObjectId(id))

# Agregar producto
@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def product(product: Product):
    if type(search_product("name", product.name)) == Product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El producto ya existe")
    
    product_dict = dict(product)
    del product_dict["id"]
    
    id = db_client.products.insert_one(product_dict).inserted_id
    
    new_product = product_schema(db_client.products.find_one({"_id": id }))
    
    return Product(**new_product)

# Actualizar producto
@router.put("/{id}", response_model=Product)
async def update_product(id: str, updated_product: Product):
    try:
        product_id = ObjectId(id)
        
        existing_product = db_client.products.find_one({"_id": product_id})
        if not existing_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
        
        updated_product_dict = dict(updated_product)
        if "id" in updated_product_dict:
            del updated_product_dict["id"]
            
        db_client.products.find_one_and_update(
            {"_id": product_id},
            {"$set": updated_product_dict},
            return_document=True
        )
        
        updated_product_data = db_client.products.find_one({"_id": product_id})
        return Product(**product_schema(updated_product_data))
    
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al actualizar el producto")

# Eliminar producto
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def product(id: str):
    
    found = db_client.products.find_one_and_delete({"_id": ObjectId(id)})
    
    if not found:
        return {"error": "No se ha eliminado el producto"}

def search_product(field: str, key):
    try:
        product = db_client.products.find_one({field: key})
        return Product(**product_schema(product))
    except:
        return {"error": "No se ha encontrado el producto"}