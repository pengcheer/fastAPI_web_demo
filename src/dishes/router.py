from typing import Literal

from fastapi import APIRouter, Depends, Path, Query
from starlette import status
from loguru import logger

from src.dishes.repository import DishRepository
from src.dishes.service import DishService
from src.dishes.schema import DishCreate, DishUpdate, DishResponse
from src.core.database import get_db


router = APIRouter(prefix="/dishes", tags=["dishes"])


# 注入仓库和服务层
async def get_dish_service(db=Depends(get_db)):
    repository = DishRepository(db)
    service = DishService(repository)
    return service


@router.post("/", response_model=DishCreate, status_code=status.HTTP_201_CREATED)
async def create_dish(
    dish_data: DishCreate, service: DishService = Depends(get_dish_service)
):
    '''创建新菜品'''
    new_dish = await service.create_dish(dish_data)
    return new_dish

@router.get("/{dish_id}", response_model=DishResponse, status_code=status.HTTP_200_OK)
async def get_dish(
    dish_id: int=Path(..., description="菜品ID"),
    service: DishService = Depends(get_dish_service),
):
    '''获取菜品信息'''
    logger.debug(f"正在获取菜品ID: {dish_id}")
    try:
        dish = await service.get_dish_by_id(dish_id)
        logger.info(f"成功获取菜品ID: {dish_id}")
        return dish
    except Exception as e:
        logger.error(f"获取菜品ID失败,{dish_id}: {e}")
        raise  # 直接抛出下层（service层）捕获的异常

@router.get("/", response_model=list[DishResponse], status_code=status.HTTP_200_OK)
async def list_dishes(
    search: str | None = Query(None, description="搜索关键词"),
    order_by: Literal["id", "name", "created_at"] = Query(None, description="排序字段"),
    direction: Literal["asc", "desc"] = Query("asc", description="排序方向，asc 或 desc"),
    limit: int = Query(10,ge=1,le=100, description="返回结果数量限制"),
    offset: int = Query(0,ge=0, description="结果偏移量"),
    service: DishService = Depends(get_dish_service),
): # 这里也可将上述查询参数构建一个pydantic模型来接收
    '''列出所有菜品'''
    dishes = await service.get_all_dishes(
        search=search,
        order_by=order_by,
        direction=direction,
        limit=limit,
        offset=offset,
    )
    return dishes   

@router.put("/{dish_id}", response_model=DishResponse, status_code=status.HTTP_200_OK)
async def update_dish(
    dish_data: DishUpdate,
    dish_id: int=Path(..., description="菜品ID"),
    service: DishService = Depends(get_dish_service),
):
    '''更新菜品信息'''
    return await service.update_dish(dish_id, dish_data)

@router.delete("/{dish_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dish(
    dish_id: int=Path(..., description="菜品ID"),
    service: DishService = Depends(get_dish_service),
):
    '''删除菜品'''
    res = await service.delete_dish(dish_id)
    return res