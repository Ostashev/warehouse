from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, CheckConstraint, Boolean
from sqlalchemy.orm import relationship
from app.core.db import Base
from datetime import datetime


class Product(Base):
    model = Column(String)
    current_status = Column(String, nullable=True)

    production_batches = relationship('ProductionBatch', back_populates='product')
    warehouse_inventory = relationship('WarehouseInventory', back_populates='product')


class ProductionBatch(Base):
    product_id = Column(
        Integer,
        ForeignKey(
            'product.id',
            name='fk_product_id'
        ),
        nullable=False
    )
    start_date = Column(DateTime, default=datetime.now)
    end_date = Column(DateTime, nullable=True)
    status = Column(String, default='start')
    warehouse = Column(Boolean, default=False)

    product = relationship('Product', back_populates='production_batches')

    __table_args__ = (
        CheckConstraint(
            "status IN ('start', 'end')",
            name='status_check'
        ),
    )
