from typing import Mapping, Any

from sqlalchemy import select, or_, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound, IntegrityError

from src.dishes.model import Dish


class DishRepository:
    """菜品仓库，封装菜品相关的数据库操作"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_dish(self, dish_data: Mapping[str, Any]) -> Dish:
        """创建新菜品"""
        new_dish = Dish(**dish_data)
        self.db_session.add(new_dish)
        try:
            await self.db_session.commit()

        except IntegrityError as e:
            await self.db_session.rollback()
            # 此处不做异常返回，业务异常返回交给服务层
            raise 
        await self.db_session.refresh(new_dish)
        return new_dish

    async def get_dish_by_id(self, dish_id: int) -> Dish | None:
        """根据ID获取菜品"""
        stmt = select(Dish).where(Dish.id == dish_id)
        result = await self.db_session.execute(stmt)
        dish = result.scalar_one_or_none()
        if not dish:
            return None
        return dish

    async def get_all_dishes(
            self,
            *,
            search: str | None = None,
            order_by: str = "id",
            direction: str = "asc",
            limit: int = 10,
            offset: int = 0,                             
        ) -> list[Dish]:
        """获取所有菜品"""
        stmt = select(Dish)

        # 1. 搜索过滤
        if search:
            stmt = stmt.where(
                or_(
                    Dish.name.ilike(f"%{search}%"),
                    Dish.description.ilike(f"%{search}%")
                )
            )
        
        # 2. 排序
        allowed_order_fields = {"id": Dish.id, "name": Dish.name, "created_at": Dish.created_at}
        if order_by not in allowed_order_fields:
            order_by = "id"  # 默认按ID排序
        order_column = getattr(Dish, order_by, Dish.id)
        stmt = stmt.order_by(
            asc(order_column) if direction == "asc" else desc(order_column))
       
        # 3. 分页
        limit = min(100, limit)
        offset = max(0, offset)
        pageinated_stmt = stmt.limit(limit).offset(offset)
        items_result = await self.db_session.scalars(pageinated_stmt)
        items = list(items_result)
        
        return items

    async def get_dish_by_name(self, name: str) -> Dish | None:
        """根据名称获取菜品"""
        stmt = select(Dish).where(Dish.name == name)
        result = await self.db_session.execute(stmt)
        dish = result.scalar_one_or_none()
        if not dish:
            return None
        return dish

    async def update_dish(self, dish_id: int, dish_data: Mapping[str, Any]) -> Dish| None:
        """更新菜品"""
        dish = await self.db_session.get(Dish, dish_id)
        if not dish:
            return None
        
        for field, value in dish_data.items():
            setattr(dish, field, value)
        self.db_session.add(dish)
        try:
            await self.db_session.commit()
        except IntegrityError as e:
            await self.db_session.rollback()
            # 此处不做异常返回，业务异常返回交给服务层
            raise 
        await self.db_session.refresh(dish)
        return dish
    
    async def delete_dish(self, dish_id: int) -> bool:
        """删除菜品"""
        dish = await self.db_session.get(Dish, dish_id)
        if not dish:
            return False
        
        await self.db_session.delete(dish)
        await self.db_session.commit()
        return True
