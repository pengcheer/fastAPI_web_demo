# src/auth/schema.py
import uuid
from datetime import datetime

from pydantic import Field
from fastapi_users.schemas import BaseUserCreate, BaseUserUpdate, BaseUser


class UserRead(BaseUser[uuid.UUID]):
    """用户读取模式"""
    name: str | None = Field(None, max_length=64, title="用户名称")
    created_at: datetime = Field(..., title="创建时间")
    updated_at: datetime = Field(..., title="最后更新时间")


class UserCreate(BaseUserCreate):
    """用户创建模式"""
    name: str | None = Field(None, max_length=64, title="用户名称")


class UserUpdate(BaseUserUpdate):
    """用户更新模式"""
    name: str | None = Field(None, max_length=64, title="用户名称")


