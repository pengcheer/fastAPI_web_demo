# src/auth/user_manager.py
import uuid

from fastapi import Depends
from fastapi_users.authentication import(
    AuthenticationBackend,
    CookieTransport, 
    BearerTransport
) 
from fastapi_users.authentication.strategy import (
    AccessTokenDatabase,
    DatabaseStrategy, 
    RedisStrategy,
)
from fastapi_users import UUIDIDMixin, BaseUserManager, FastAPIUsers
from fastapi_users.db import SQLAlchemyUserDatabase
from redis.asyncio import Redis

from src.core.config import settings
from src.core.redis_db import get_auth_redis
from src.auth.dependencies import get_access_token_db, get_user_db
from src.auth.model import User, AccessToken


## -----------传输方式------------------
# cookie 传输方式
cookie_transport = CookieTransport(cookie_name="auth_cookie")

# bearer 传输方式
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

## -----------策略 ------------------
# 数据库策略
def get_database_strategy(
        access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db)
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, lifetime_seconds=3600)  # 1 hour

# redis 策略（可选）
# 需要启动redis服务，并安装做好模型配置
def get_redis_strategy(
        redis: Redis = Depends(get_auth_redis)
) -> RedisStrategy:
    return RedisStrategy(redis, lifetime_seconds=3600)


##  -----------认证后端 ------------------
# 基于数据库的认证后端
database_auth_backend = AuthenticationBackend(
    name = "database",
    transport = cookie_transport,
    get_strategy = get_database_strategy,
)

# 基于 Redis 的认证后端（可选）
redis_auth_backend = AuthenticationBackend(
    name = "redis",
    transport = bearer_transport,
    get_strategy = get_redis_strategy,
)

# 根据需求选择使用单个Secret Key或拆分为多个
# 分别用于重设密码和电子邮件验证等功能
SECRET_KEY = settings.jwt_secret


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    """用户管理器，处理用户相关操作，如注册、验证等"""
    reset_password_token_secret = SECRET_KEY
    verification_token_secret = SECRET_KEY

    async def on_after_register(self, user: User, request=None):
        """用户注册后触发的操作"""
        print(f"用户 {user.id} 已注册。")

    async def on_after_forgot_password(
        self, user: User, token: str, request=None
    ):
        """用户请求重设密码后触发的操作"""
        print(f"用户 {user.id} 请求重设密码。重设令牌：{token}")

    async def on_after_request_verify(
        self, user: User, token: str, request=None
    ):
        """用户请求验证电子邮件后触发的操作"""
        print(f"用户 {user.id} 请求验证电子邮件。验证令牌：{token}")

# 用户管理器的依赖项
async def get_user_manager(
        user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
) -> UserManager: # type: ignore
    yield UserManager(user_db) # type: ignore


# FastAPI Users 实例
fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [database_auth_backend, redis_auth_backend],
)

# 默认获取当前活动用户
current_active_user = fastapi_users.current_user(active=True)

# --其他可选的依赖项--
# 获取当前超级用户
current_superuser = fastapi_users.current_user(superuser=True)
# 获取当前已验证的用户
current_verified_user = fastapi_users.current_user(verified=True)