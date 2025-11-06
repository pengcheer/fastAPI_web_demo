# src/core/redis_db.py
from typing import cast

from fastapi import Request
from redis.asyncio import Redis

from src.core.config import settings


def create_auth_redis() -> Redis:
    """创建并返回一个 Redis 客户端实例"""
    return Redis.from_url(
        settings.auth_redis_url,
        max_connections=20,
        decode_responses=True,
    )

def create_cache_redis() -> Redis:
    """创建并返回一个用于缓存的 Redis 客户端实例   """
    return Redis.from_url(
        settings.cache_redis_url,
        max_connections=20,
        decode_responses=True,
    )


async def get_auth_redis(request: Request) -> Redis:
    """FastAPI 依赖项，用于获取认证 Redis 客户端实例"""
    return cast(Redis, request.state.auth_redis)

async def get_cache_redis(request: Request) -> Redis:
    """FastAPI 依赖项，用于获取缓存 Redis 客户端实例"""
    return cast(Redis, request.state.cache_redis)