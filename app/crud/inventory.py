from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.crudBase import CRUDBase
from app.models import WarehouseInventory


class CRUDInventory(CRUDBase):
    async def get_by_prouct_id(
            self,
            product_id: int,
            session: AsyncSession,
    ) -> WarehouseInventory:
        db_obj = await session.execute(
            select(WarehouseInventory).where(
                WarehouseInventory.product_id == product_id
            )
        )
        db_obj = db_obj.scalar()
        if db_obj is None:
            raise HTTPException(status_code=404, detail='Объект не найден')
        return db_obj


inventory_crud = CRUDInventory(WarehouseInventory)
