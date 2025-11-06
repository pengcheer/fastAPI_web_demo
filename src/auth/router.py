# src/auth/router.py
from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from src.auth.user_manager import redis_auth_backend,database_auth_backend
from src.auth.schema import UserRead, UserCreate, UserUpdate


def register_fastapi_users_router(
        app: FastAPI,
        fastapi_users:FastAPIUsers,
):
    """把FastAPI-Users的所有router 挂载到 app上"""
    # 运用bearer传输方式
    app.include_router(
        fastapi_users.get_auth_router(redis_auth_backend), #requires_verification=True
        prefix="/auth/jwt",
        tags=["auth"],
    )
    # 用于cookie传输
    app.include_router(
        fastapi_users.get_auth_router(database_auth_backend),
        prefix="/auth/cookie",
        tags=["auth"],
    )

    app.include_router(
        fastapi_users.get_register_router(UserRead,UserCreate),
        prefix="/auth",
        tags=["auth"],
    )

    app.include_router(
        fastapi_users.get_reset_password_router(),
        prefix="/auth",
        tags=["auth"],
    )

    app.include_router(
        fastapi_users.get_verify_router(UserRead),
        prefix="/auth",
        tags=["auth"],
    )

    app.include_router(
        fastapi_users.get_users_router(UserRead, UserUpdate),
        prefix="/users",
        tags=["users"],
    )