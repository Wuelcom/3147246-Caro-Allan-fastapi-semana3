from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

# ----- MODELOS -----
class Book(BaseModel):
    id: int
    title: str
    author: str
    genre: str
    year: int
    available: bool = True

class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    year: int

# ----- BASE DE DATOS EN MEMORIA -----
books_db: List[Book] = [
    Book(id=1, title="Cien años de soledad", author="Gabriel García Márquez", genre="Novela", year=1967),
    Book(id=2, title="Don Quijote de la Mancha", author="Miguel de Cervantes", genre="Clásico", year=1605),
]

# ----- ENDPOINTS -----
@router.get("/books", response_model=List[Book])
def get_books():
    return books_db

@router.post("/books", response_model=Book)
def add_book(book: BookCreate):
    new_id = max(b.id for b in books_db) + 1 if books_db else 1
    new_book = Book(id=new_id, **book.model_dump())
    books_db.append(new_book)
    return new_book

@router.post("/borrowing/borrow/{book_id}", response_model=Book)
def borrow_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            if not book.available:
                raise HTTPException(status_code=400, detail="Libro no disponible")
            book.available = False
            return book
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@router.post("/borrowing/return/{book_id}", response_model=Book)
def return_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            book.available = True
            return book
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@router.get("/categories", response_model=List[str])
def list_genres():
    return list(set([b.genre for b in books_db]))