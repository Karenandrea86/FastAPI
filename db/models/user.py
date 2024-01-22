from pydantic import BaseModel

# Entidad user
class User(BaseModel):
    id: str | None = None
    username: str
    email: str