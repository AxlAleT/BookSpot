from fastapi import APIRouter, Depends, HTTPException, status
from app.core.base import SessionLocal  # Importamos SessionLocal desde core/database.py
from . import schemas
from compartido import modelos

router = APIRouter()

@router.post("/sales/", response_model=schemas.SaleResponse)
def create_sale(sale_request: schemas.SaleRequest):
    # Usamos un bloque with para crear y cerrar la sesión automáticamente
    with SessionLocal() as db:  
        books_response = []
        for item in sale_request.items:
            book = db.query(modelos ).filter(models.Book.id == item.book_id).first()
            if not book:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book not found with id: {item.book_id}")
            available_quantity = min(item.quantity, book.stock)
            if available_quantity > 0:
                books_response.append(schemas.BookResponse(
                    title=book.title,
                    id=book.id,
                    price=book.price,
                    quantity=available_quantity
                ))
    return schemas.SaleResponse(books=books_response)
