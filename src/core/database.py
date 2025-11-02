from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from loguru import logger

from src.core.config import settings
from src.core.model import Base
from src.dishes.model import Dish  # 确保模型已导入以创建表

# 创建异步引擎
# print(f"数据库连接字符串: {settings.database_url}")
engine = create_async_engine(settings.database_url, **settings.engine_options)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
    bind=engine
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """获取数据库会话的异步生成器，使用依赖注入时推荐使用此函数"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"数据库会话发生错误: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()



# 用于临时性脚本的数据库创建函数
# 请在生产环境中使用Alembic进行数据库迁移
async def creat_db_and_tables():
    """初始化数据库，创建所有表"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(Dish.metadata.create_all)  # 确保Dish表被创建

    logger.info("数据库初始化完成，所有表已创建。")
