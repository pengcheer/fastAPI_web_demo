# src/lifespan.py
from typing import TypedDict
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from redis.asyncio import Redis

from src.core.redis_db import create_auth_redis, create_cache_redis
# from src.core.database import creat_db_and_tables


# 定义一个Redis状态类型字典
class State(TypedDict):
    auth_redis: Redis
    cache_redis: Redis
    

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[State]:
    """应用生命周期管理器，负责在应用启动和关闭时执行特定操作"""
    # 应用启动时执行的操作
    logger.info("应用启动，开始加载所有资源")

    # 初始化数据库（仅用于开发和测试环境，已启用并修改为 Alembic 进行迁移）
    # await creat_db_and_tables()
    # logger.info("数据库初始化完成。")

    auth_redis = create_auth_redis()
    cache_redis = create_cache_redis()
    logger.info("Redis 客户端初始化完成。")

    # 这里是应用运行的时间段
    yield  State(auth_redis=auth_redis, cache_redis=cache_redis) 

    #----------关闭 ----------------
    await auth_redis.close()
    await cache_redis.close()

    # 应用关闭时执行的操作
    logger.info("应用关闭,资源释放...")
