# src/auth/model.py
from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTableUUID

from src.core.model import Base, DateTimeMixin


class User(SQLAlchemyBaseUserTableUUID, DateTimeMixin, Base):
    """用户模型"""
    # SQLAlchemyBaseUserTableUUID 已经定义了 id、email、hashed_password、is_active、is_superuser、is_verified字段
    # 可根据需要添加其他字段
    name: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="用户名称")

    # 可选：定义与其他模型的关系
    # dishes: Mapped[list["Dish"]] = relationship("Dish", back_populates="owner")


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    """访问令牌模型"""
    # SQLAlchemyBaseAccessTokenTableUUID 已经定义了 id、user_id、token、expires_at字段
    pass