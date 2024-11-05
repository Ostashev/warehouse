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
