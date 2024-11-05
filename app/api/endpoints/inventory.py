import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.batch import batch_crud
from app.crud.inventory import inventory_crud
from app.crud.product import product_crud
from app.schemas.inventory import InventoryResponse, Inventory


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
