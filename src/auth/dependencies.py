# src/auth/dependencies.py
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase

from src.core.database import get_db
from src.auth.model import User, AccessToken


"""用户认证相关的依赖项定义，包括用户数据库和访问令牌数据库的依赖注入"""

# 获取用户数据库的依赖项
async def get_user_db(
    session: AsyncSession = Depends(get_db),
) : 
    yield SQLAlchemyUserDatabase(session, User) 


# 获取访问令牌数据库的依赖项
async def get_access_token_db(
    session: AsyncSession = Depends(get_db),
) : 
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken) 