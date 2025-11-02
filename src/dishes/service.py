# src/dishes/service.py
from sqlalchemy.exc import IntegrityError

from src.core.exception import AlreadyExistsException, NotFoundException
from src.dishes.repository import DishRepository
from src.dishes.schema import (
    DishCreate, 
    DishUpdate, 
    DishResponse
)


class DishService:
    """菜品服务，封装菜品相关的业务逻辑[目前仅做校验和异常捕捉]"""

    def __init__(self, repository: DishRepository):
        self.repository = repository

    async def create_dish(self, dish_create: DishCreate) -> DishResponse:
        """创建新菜品,处理唯一性约束异常"""
        try:
            new_dish = await self.repository.create_dish(dish_create.model_dump())
        except IntegrityError as e:
            # 数据库唯一性约束异常 -> 业务异常
            raise AlreadyExistsException("菜品名称已存在") from e
        return DishResponse.model_validate(new_dish)

    async def get_dish_by_id(self, dish_id: int) -> DishResponse:
        """根据ID获取菜品"""
        dish = await self.repository.get_dish_by_id(dish_id)
        if not dish:
            raise NotFoundException("未找到ID为{dish.id}对应的菜品")
        return DishResponse.model_validate(dish) 
        
    async def get_all_dishes(
        self,
        *,
        search: str | None = None,
        order_by: str = "id",
        direction: str = "asc",
        limit: int = 10,
        offset: int = 0,
    ) -> list[DishResponse]:
        """获取所有菜品"""
        dishes = await self.repository.get_all_dishes(
            search=search,
            order_by=order_by,
            direction=direction,
            limit=limit,
            offset=offset,
        )
        return [DishResponse.model_validate(dish) for dish in dishes]

    async def update_dish(self, dish_id: int, dish_update: DishUpdate) -> DishResponse:
        """更新菜品"""
        try:
            update_data = dish_update.model_dump(exclude_unset=True, exclude_none=True)
            updated = await self.repository.update_dish(dish_id, update_data)
            if not updated:
                raise NotFoundException(f"未找到ID为{dish_id}对应的菜品")
            return DishResponse.model_validate(updated)
        except IntegrityError as e:
            raise AlreadyExistsException("菜品名称已存在") from e
    
    async def delete_dish(self, dish_id: int) -> None:
        """删除菜品"""
        deleted = await self.repository.delete_dish(dish_id)
        if not deleted:
            raise NotFoundException(f"未找到ID为{dish_id}对应的菜品")
