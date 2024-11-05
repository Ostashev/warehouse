import logging
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func, or_, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, aliased

from app.core.config import settings
from app.core.db import get_async_session
from app.models import *
from app.crud.product import product_crud
from app.schemas.product import ProductDB
from app.core.cache import get_cached_data, set_cached_data

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.get('/all',
            response_model=List[ProductDB],
            response_model_exclude_none=True,
            status_code=HTTPStatus.OK,
            summary="Получение списка всех товаров.",
            )
async def get_products(
        session: AsyncSession = Depends(get_async_session),
) -> List[ProductDB]:
    logger.info("Запрос на получение продуктов")

    cache_key = "all_products"

    # Проверяем кэш
    cached_data = get_cached_data(cache_key)
    if cached_data is not None:
        logger.info("Данные получены из кэша")
        # Преобразуем кэшированные данные обратно в объекты ProductDB
        return [ProductDB.parse_obj(item) for item in cached_data]

    try:
        # Получаем данные из базы данных
        products = await product_crud.get_multi(session)

        # Преобразуем продукты в модели Pydantic
        products_data = [ProductDB.from_orm(product) for product in products]

        # Сохраняем данные в кэш, преобразуя в JSON
        set_cached_data(cache_key, [product.dict() for product in products_data])

        logger.info("Продукты успешно получены и сохранены в кэше")
        return products_data
    except HTTPException as e:
        logger.error(f"Ошибка при получении продуктов: {e.detail}")
        raise e
    except Exception as e:
        logger.exception("Непредвиденная ошибка при получении продуктов")
        raise HTTPException(status_code=500, detail="Произошла непредвиденная ошибка")


@router.get('/{product_id}',
            response_model=ProductDB,
            response_model_exclude_none=True,
            status_code=HTTPStatus.OK,
            summary="Получение информации о конкретном товаре.",
            )
async def get_product(
        product_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> ProductDB:
    logger.info(f"Запрос на получение продукта с product_id={product_id}")
    cache_key = f"product_{product_id}"

    # Проверяем кэш
    cached_data = get_cached_data(cache_key)
    if cached_data is not None:
        logger.info(f"Данные для product_id={product_id} получены из кэша")
        return ProductDB.parse_obj(cached_data)
    try:
        product = await product_crud.get(product_id, session)
        logger.info(f"Продукт с product_id={product_id} успешно получен")

        set_cached_data(cache_key, ProductDB.from_orm(product).dict())
        return product
    except HTTPException as e:
        logger.error(f"Ошибка при получении продукта с product_id={product_id}: {e.detail}")
        raise e
    except Exception as e:
        logger.exception(f"Непредвиденная ошибка при получении продукта с product_id={product_id}")
        raise HTTPException(status_code=500, detail="Произошла непредвиденная ошибка")



