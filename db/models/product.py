from pydantic import BaseModel

# Entidad product
class Product(BaseModel):
    id: str | None = None
    name: str
    description: str