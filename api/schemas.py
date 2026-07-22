from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class BookCreate(BaseModel):
    isbn: str
    title: str
    author: str
    category: str
    copies: int

class BookOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    isbn: str
    title: str
    author: str
    category: str
    total_copies: int
    borrowed_copies: int
    available_copies: int

class UserCreate(BaseModel):
    user_id: str
    name: str
    username: str

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    username: str

class BorrowRequest(BaseModel):
    title: str
    username: str

class ReturnRequest(BaseModel):
    title: str
    username: str

class BorrowRecordOut(BaseModel):
    username: str
    book_title: str
    borrow_date: datetime

    