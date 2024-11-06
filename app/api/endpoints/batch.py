import logging
from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.batch import batch_crud
from app.crud.product import product_crud
from app.schemas.batch import (BatchCreate, BatchDB, BatchUpdate, BatchUpdated,
                               BatchUpdateStage)

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post('/batches',
             response_model=BatchDB,
             status_code=HTTPStatus.CREATED,
             summary='Создать новую партию',
             )
async def create_batch(
        batch: BatchCreate,
        session: AsyncSession = Depends(get_async_session),
) -> BatchDB:
    logger.info(f'Попытка создания новой партии для продукта с ID: {batch.product_id}')
    await product_crud.get(batch.product_id, session)
    new_batch = await batch_crud.create(batch, session)
    logger.info(f'Партия создана.')
    return new_batch


@router.patch('/batches/{batch_id}/stages',
              response_model=BatchUpdated,
              status_code=HTTPStatus.OK,
              summary='Редактировать статус партии',
              )
async def update_batch(
        batch_id: int,
        batch: BatchUpdateStage,
        session: AsyncSession = Depends(get_async_session),
) -> BatchUpdated:
    logger.info(f'Попытка обновления статуса партии с ID: {batch_id}')
    batch_db = await batch_crud.get(batch_id, session)
    if batch_db.status == 'end':
        logger.warning(f'Попытка обновления завершенной партии с ID: {batch_id}')
        raise HTTPException(status_code=409, detail='Партия уже завершена.')
    update_batch = BatchUpdate(
        end_date=datetime.now(),
        status=batch.new_stage
    )
    batch = await batch_crud.update(obj_in=update_batch, db_obj=batch_db, session=session)
    message = 'Статус успешно обновлен'
    product = await product_crud.get(batch.product_id, session)
    if product.current_status == 'OUT_OF_STOCK':
        product.current_status = 'IN_PRODUCTION'
        await session.commit()

    logger.info(f'Статус партии с ID {batch_id} успешно обновлен на "end"')
    return BatchUpdated(message=message, updated_batch=batch)
