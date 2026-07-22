from fastapi import APIRouter, HTTPException
from typing import List
from services.library_service import LibraryService
from api.schemas import BorrowRequest, ReturnRequest, BorrowRecordOut

router = APIRouter(tags=["borrowing"])
service = LibraryService()

@router.post("/borrow")
def borrow_book(payload: BorrowRequest):
    try:
        service.borrow_book(payload.title, payload.username)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"detail": "Book borrowed successfully"}

@router.post("/return")
def return_book(payload: ReturnRequest):
    try:
        service.return_book(payload.title, payload.username)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"detail": "Book returned successfully"}

@router.get("/borrowed", response_model=List[BorrowRecordOut])
def list_borrowed():
    records = service.get_all_borrowed_records()
    return [
        BorrowRecordOut(username=r.user.username, book_title=r.book.title, borrow_date=r.borrow_date)
        for r in records
    ]

    