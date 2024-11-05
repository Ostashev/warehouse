from pydantic import BaseModel


class ProductDB(BaseModel):
    id: int
    model: str
    current_status: str

    class Config:
        orm_mode = True
