import logging
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.batch import batch_crud
from app.crud.inventory import inventory_crud
from app.crud.product import product_crud
from app.schemas.inventory import (InventorProducts, Inventory,
                                   InventoryResponse, Shipment,
                                   ShipmentProduct, ShipmentResponse)

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.put('/receive-batch/{batch_id}',
            response_model=InventoryResponse,
            status_code=HTTPStatus.OK,
            summary='Приемка готовой партии товара на склад',
            )
async def update_inventory(
        batch_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> InventoryResponse:
    logger.info(f'Попытка принять партию с ID: {batch_id}')
    batch = await batch_crud.get(batch_id, session)

    if batch.status != 'end':
        logger.warning(f'Попытка принять не завершенную партию с ID: {batch_id}')
        raise HTTPException(status_code=409, detail="Партия еще не завершена.")

    if batch.warehouse == True:
        logger.warning(f'Партия с ID: {batch_id} уже принята на склад.')
        raise HTTPException(status_code=409, detail='Партия уже принята на склад.')

    obj = await inventory_crud.get_by_prouct_id(batch.product_id, session)
    product = await product_crud.get(batch.product_id, session)
    obj.quantity += 1
    batch.warehouse = True
    if product.current_status != 'IN_STOCK':
        product.current_status = 'IN_STOCK'
    await session.commit()
    await session.refresh(obj)

    message = 'Партия принята на склад.'
    logger.info(f'Партия с ID: {batch_id} успешно принята на склад.')

    return InventoryResponse(
        message=message,
        inventory=Inventory(
            id=obj.id,
            product_id=obj.product_id,
            model=product.model,
            location=obj.location,
            quantity=obj.quantity
        )
    )


@router.post('/shipments',
             response_model=ShipmentResponse,
             status_code=HTTPStatus.CREATED,
             summary='Оформление отгрузки товара клиенту.',
             )
async def create_shipment(
        shipment: Shipment,
        session: AsyncSession = Depends(get_async_session),
) -> ShipmentResponse:
    logger.info(f'Попытка отгрузки товара клиенту.')

    product_counts = {}
    bad_result = []

    for item in shipment.items:
        product_id = item.product_id
        if product_id in product_counts:
            product_counts[product_id] += 1
        else:
            product_counts[product_id] = 1

    for product_id, count in product_counts.items():
        inventory = await inventory_crud.get(product_id, session)

        if count < inventory.quantity:
            inventory.quantity -= count
        elif count == inventory.quantity:
            inventory.quantity -= count
            product = await product_crud.get(product_id, session)
            product.current_status = 'OUT_OF_STOCK'
        else:
            bad_result.append(
                f'Недостаточно товара с ID {product_id}. Требуется: {count}, доступно: {inventory.quantity}.'
            )
    if bad_result:
        logger.error(f'Ошибки при оформлении отгрузки: {"; ".join(bad_result)}')
        raise HTTPException(status_code=409, detail="; ".join(bad_result))
    await session.commit()
    logger.info(f'Отгрузка товара для заказа {shipment.order} успешно оформлена.')

    result = ShipmentResponse(
        order=shipment.order,
        items=[ShipmentProduct(product_id=item.product_id) for item in shipment.items],
        status='SHIPPED'
    )

    return result


@router.get('/inventory',
            response_model=List[InventorProducts],
            status_code=HTTPStatus.OK,
            summary='Получение текущих остатков товаров на складе.',
            )
async def get_inventory(
        session: AsyncSession = Depends(get_async_session),
) -> List[InventorProducts]:
    logger.info('Запрос на получение текущих остатков товаров на складе.')
    inventories = await inventory_crud.get_inventories(session)
    logger.info(f'Получено {len(inventories)} записей об остатках товаров на складе.')
    return inventories
