# Users DB API

from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())

# Path
@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))

# Query    
@router.get("/")
async def user():
    return search_user("_id", ObjectId(id))

# Agregar usuario
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email", user.email))  == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
        
    user_dict = dict(user)
    del user_dict["id"]
    
    id = db_client.users.insert_one(user_dict).inserted_id
    
    new_user = user_schema(db_client.users.find_one({"_id": id}))
    
    return User(**new_user)
        
# Actualizar usuario
@router.put("/{id}", response_model=User)
async def update_user(id: str, updated_user: User):
    try:
        user_id = ObjectId(id)

        existing_user = db_client.users.find_one({"_id": user_id})
        if not existing_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

        updated_user_dict = dict(updated_user)
        if "id" in updated_user_dict:
            del updated_user_dict["id"]

        db_client.users.find_one_and_update(
            {"_id": user_id},
            {"$set": updated_user_dict},
            return_document=True
        )

        updated_user_data = db_client.users.find_one({"_id": user_id})
        return User(**user_schema(updated_user_data))
        
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al actualizar el usuario")

# Eliminar usuario
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
            
    if not found:
        return {"error": "No se ha eliminado el usuario"}
    
def search_user(field: str, key):
    try:
        user = db_client.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error": "No se ha encontrado el usuario"}