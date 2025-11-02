from datetime import datetime
from pydantic import BaseModel, Field
from typing import Annotated, Optional


#公共字段基类
class DishBase(BaseModel):
    """菜品基础模型"""
    name: str = Field(..., description="菜品名称", max_length=100)
    description: Annotated[Optional[str], Field(description="菜品描述", max_length=500)] = None


#创建菜品请求模型
class DishCreate(DishBase):
    """创建菜品请求模型"""
    pass


#更新菜品请求模型
class DishUpdate(BaseModel):
    """更新菜品请求模型"""
    name: Annotated[Optional[str], Field(description="菜品名称", max_length=100)] = None
    description: Annotated[Optional[str], Field(description="菜品描述", max_length=500)] = None


#响应模型
class DishResponse(DishBase):
    """菜品响应模型"""
    id: int = Field(..., description="菜品ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="最后更新时间")

    model_config = {
        "from_attributes": True  # 允许从 ORM 模型实例创建 Pydantic
    }


# 查询参数模型
class DishQueryParams(BaseModel):
    """菜品查询参数模型"""
    search: Annotated[Optional[str], Field(description="搜索关键词")] = None
    order_by: Annotated[Optional[str], Field(description="排序字段，可选值：id, name, created_at")] = None
    direction: str = Field("asc", description="排序方向，asc 或 desc")
    limit: int = Field(10, ge=1, le=100, description="返回结果数量限制")
    offset: int = Field(0, ge=0, description="结果偏移量")
    

