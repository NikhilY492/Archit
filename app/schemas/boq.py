from pydantic import BaseModel
from typing import List


class BOQLineItem(BaseModel):
    description: str
    quantity: float
    unit: str
    rate: float
    amount: float


class BOQResult(BaseModel):
    items: List[BOQLineItem]
    subtotal: float
