from typing import Optional

from pydantic import BaseModel, validator
from datetime import datetime


class BatchCreate(BaseModel):
    product_id: int


class BatchDB(BaseModel):
    id: int
    product_id: int
    start_date: datetime
    end_date: Optional[datetime] = None
    status: str

    class Config:
        orm_mode = True


class BatchUpdateStage(BaseModel):
    new_stage: str

    @validator('new_stage')
    def validate_stage(cls, value):
        if value != 'end':
            raise ValueError("new_stage должен быть 'end'")
        return value


class BatchUpdate(BaseModel):
    end_date: datetime
    status: str


class BatchUpdated(BaseModel):
    message: str
    updated_batch: BatchDB
