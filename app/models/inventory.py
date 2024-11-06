from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.db import Base


class WarehouseInventory(Base):
    product_id = Column(
        Integer,
        ForeignKey(
            'product.id',
            name='fk_product_id_warehouse_inventory'
        ),
        nullable=False
    )
    quantity = Column(Integer, default=0)
    location = Column(String)

    product = relationship('Product', back_populates='warehouse_inventory')

    __table_args__ = (
        CheckConstraint(
            'quantity >= 0',
            name='quantity_non_negative'
        ),
    )
