from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int
    
users_list = [
    User(
        id= 1,
        name="Karen",
        surname="Velasquez",
        url="https://karenavh123.com",
        age=19
    ),
    User(
        id= 2,
        name= "Andrea",
        surname= "Hueso",
        url= "https://kandreavh123.com",
        age= 19
    )
]

@router.get("/usersjson")
async def usersjson():
    return [
        {
            "name": "Karen",
            "surname": "Velasquez",
            "url": "https://karenavh123.com",
            "age": 19
            },
        {
            "name": "Andrea",
            "surname": "Hueso",
            "url": "https://kandreavh123.com",
            "age": 19
        }
        ]

@router.get("/users")
async def users():
    return users_list

# Path
@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)

# Query    
@router.get("/user/")
async def user(id: int):
    return search_user(id)

# Agregar usuario
@router.post("/user/", response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id))  == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
    
    users_list.append(user)
    return user
        
# Actualizar usuario
@router.put("/user/")
async def user(user: User):
    
    found = False
    
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
            
    if not found:
        return{"error": "No se ha actualizado el usuario"}
    
    return user

# Eliminar usuario
@router.delete("/user/{id}")
async def user(id: int):
    
    found = False
    
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
            
    if not found:
        return {"error": "No se ha eliminado el usuario"}
    
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}