from pydantic import BaseModel
from typing import List

class BookItem(BaseModel):
    book_id: int
    quantity: int

class BookResponse(BaseModel):
    title: str
    id: int
    price: float
    quantity: int

class SaleRequest(BaseModel):
    items: List[BookItem]

class SaleResponse(BaseModel):
    books: List[BookResponse]
