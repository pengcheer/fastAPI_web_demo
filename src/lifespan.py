# src/lifespan.py
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from src.core.database import creat_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """应用生命周期管理器，负责在应用启动和关闭时执行特定操作"""
    # 应用启动时执行的操作
    logger.info("应用启动，开始加载所有资源")

    # 初始化数据库（仅用于开发和测试环境，生产环境请使用 Alembic 进行迁移）
    await creat_db_and_tables()
    logger.info("数据库初始化完成。")

    yield  # 这里是应用运行的时间段

    # 应用关闭时执行的操作
    logger.info("应用关闭,资源释放...")
