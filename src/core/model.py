
from datetime import datetime, timezone

from sqlalchemy import MetaData, func, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.core.config import settings


# 全局命名规范，确保数据库对象命名一致且易于识别
database_naming_convention = {
    "ix": "ix_%(column_0_label)s_idx",
    "uq": "uq_%(table_name)s_%(column_0_name)s_key",
    "ck": "ck_%(table_name)s_%(constraint_name)s_check",  
    "fk": "fk_%(table_name)s_%(column_0_name)s_fkey",
    "pk": "pk_%(table_name)s_pkey",
}


class Base(DeclarativeBase):
    """全局统一"""
    matadata = MetaData(naming_convention=database_naming_convention)


class DateTimeMixin:
    """包含创建和更新时间戳的混入类"""
    match settings.db_type:
        case "postgres":
            created_at: Mapped[datetime] = mapped_column(
                DateTime(timezone=True),
                server_default=func.now(),
                nullable=False,
                doc="记录创建时间，UTC 时间",
            )
            updated_at: Mapped[datetime] = mapped_column(
                DateTime(timezone=True),
                server_default=func.now(),
                onupdate=func.now(),
                nullable=False,
                doc="记录最后更新时间，UTC 时间",
            )
        case "sqlite":
            created_at: Mapped[datetime] = mapped_column(
                DateTime(timezone=True),
                # SQLite 不支持 server_default=func.now()，只能用 Python 端设置默认值
                # 插入时采用应用层时间，生产环境中建议使用unix时间戳
                default=lambda: datetime.now(timezone.utc),
                nullable=False,
                index=True,
                doc="记录创建时间，UTC 时间",
            )
            updated_at: Mapped[datetime] = mapped_column(
                DateTime(timezone=True),
                default=lambda: datetime.now(timezone.utc),
                onupdate=lambda: datetime.now(timezone.utc),
                nullable=False,
                index=True,
                doc="记录最后更新时间，UTC 时间",
            )
        case _:
            raise ValueError(f"Unsupported DB_TYPE: {settings.db_type}")
