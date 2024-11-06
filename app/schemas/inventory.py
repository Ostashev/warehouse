from typing import List

from pydantic import BaseModel


class Inventory(BaseModel):
    id: int
    product_id: int
    model: str
    location: str
    quantity: int


class InventoryResponse(BaseModel):
    message: str
    inventory: Inventory


class ShipmentProduct(BaseModel):
    product_id: int


class Shipment(BaseModel):
    order: str
    items: List[ShipmentProduct]


class ShipmentResponse(BaseModel):
    order: str
    items: List[ShipmentProduct]
    status: str


class InventorProducts(BaseModel):
    product_id: int
    model: str
    quantity: int
