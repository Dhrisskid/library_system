from fastapi import APIRouter, HTTPException
from typing import List, Optional
from services.library_service import LibraryService
from api.schemas import BookCreate, BookOut

router = APIRouter(prefix="/books", tags=["books"])
service = LibraryService()

@router.post("", response_model=BookOut)
def add_book(payload: BookCreate):
    try:
        service.add_book(payload.isbn, payload.title, payload.author, payload.category, payload.copies)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return service.search_book_by_isbn(payload.isbn)

@router.get("", response_model=List[BookOut])
def list_books():
    return service.book_repo.get_all()

@router.get("/search", response_model=List[BookOut])
def search_books(title: Optional[str] = None, author: Optional[str] = None, category: Optional[str] = None):
    if title:
        return service.search_books_by_title(title)
    if author:
        return service.search_books_by_author(author)
    if category:
        return service.search_books_by_category(category)
    raise HTTPException(status_code=400, detail="Provide title, author, or category")

@router.get("/{isbn}", response_model=BookOut)
def get_book(isbn: str):
    book = service.search_book_by_isbn(isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.delete("/{isbn}")
def delete_book(isbn: str):
    try:
        service.delete_book(isbn)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"detail": "Book deleted successfully"}

    