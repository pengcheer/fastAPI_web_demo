from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.core.model import Base, DateTimeMixin


class Dish(Base, DateTimeMixin):
    __tablename__ = "dishes"

    # 实际项目使用时id建议使用 UUID 或雪花算法生成的分布式ID
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, doc="菜品ID")
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, doc="菜品名称")
    description: Mapped[str] = mapped_column(Text, nullable=True, doc="菜品描述")