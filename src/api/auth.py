from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException
from src.schemas.users import UserAdd, UserInDB, UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])


@router.post("/register")
async def register_user(data: UserRequestAdd, db: DBDep):
    hash_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hash_password)
    try:
        await db.users.add(new_user_data)
        await db.commit()
    except ObjectNotFoundException:
        raise HTTPException(status_code=409, detail="Пользователь уже зарегистрирован")

    return {"status": "OK"}


@router.post("/login")
async def login_user(data: UserRequestAdd, responce: Response, db: DBDep):
    user: UserInDB | None = await db.users.get_user_with_hashed_password(
        email=data.email
    )
    if not user or not AuthService().verify_password(
        data.password, user.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    access_token = AuthService().create_access_token({"user_id": user.id})
    responce.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/only_auth")
async def only_auth(user_id: UserIdDep, db: DBDep):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.post("/logout")
async def logout_user(responce: Response):
    responce.delete_cookie("access_token")
    return {"status": "OK"}
