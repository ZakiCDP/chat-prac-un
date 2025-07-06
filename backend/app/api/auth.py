from fastapi import APIRouter

# Need to improve code below

# POST
@router.post("/auth/register")
def register():
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    return username, password

@router.post("/auth/login")
def login(username, password):
    if len(username) < 5 or len(password) < 5:
        return False
    elif len(username) > 15 or len(password) > 15:
        return False
    elif not any(char.isdigit() for char in password):
        return False
    elif not any(char.isupper() for char in password):
        return False

# GET
@router.get("/me")
async def get_profile(token: str = Depends(oauth2_scheme)):
    # Логика получения данных текущего пользователя
    return {
        "username": "test_user",
        "joined_at": "2023-01-01"
    }

# PATCH
@router.patch("/me")
async def update_profile():
    # Редактирование профиля
    pass