from models.book import Book
from models.user import User
from models.borrow_record import BorrowRecord
from repositories.book_repo import BookRepository
from repositories.user_repo import UserRepository
from repositories.borrow_repo import BorrowRepository
from datetime import datetime, timezone
from typing import List, Optional

class LibraryService:
    def __init__(self):
        self.book_repo = BookRepository()
        self.user_repo = UserRepository()
        self.borrow_repo = BorrowRepository()

    def add_book(self, isbn: str, title: str, author: str, category: str, copies: int):
        if copies <= 0:
            raise ValueError("Number of copies must be positive")
        if self.book_repo.book_exists(isbn):
            raise ValueError("Book with this ISBN already exists")
        book = Book(isbn=isbn, title=title, author=author, category=category,
                    total_copies=copies, borrowed_copies=0)
        if not self.book_repo.create(book):
            raise ValueError("Failed to add book")

    def register_user(self, user_id: str, name: str, username: str):
        if self.user_repo.get_by_id(user_id):
            raise ValueError("User ID already exists")
        if self.user_repo.get_by_username(username):
            raise ValueError("Username already exists")
        user = User(id=user_id, name=name, username=username)
        if not self.user_repo.create(user):
            raise ValueError("Failed to register user")

    def borrow_book(self, book_title: str, username: str):
        user = self.user_repo.get_by_username(username)
        if not user:
            raise ValueError("User not found")

        books = self.book_repo.search_by_title(book_title)
        if not books:
            raise ValueError("Book not found")

        book = None
        for b in books:
            if b.title.lower() == book_title.lower():
                book = b
                break
        if not book:
            raise ValueError("Book not found")

        if book.available_copies <= 0:
            raise ValueError("No copies available")
        active = self.borrow_repo.find_active_borrow(user.id, book.isbn)
        if active:
            raise ValueError("User already borrowed this book")

        if not book.borrow_copy():
            raise ValueError("Failed to borrow book")
        self.book_repo.update(book)

        record = BorrowRecord(user_id=user.id, book_isbn=book.isbn)
        if not self.borrow_repo.create(record):
            raise ValueError("Failed to create borrow record")

    def return_book(self, book_title: str, username: str):
        user = self.user_repo.get_by_username(username)
        if not user:
            raise ValueError("User not found")

        books = self.book_repo.search_by_title(book_title)
        if not books:
            raise ValueError("Book not found")
        book = None
        for b in books:
            if b.title.lower() == book_title.lower():
                book = b
                break
        if not book:
            raise ValueError("Book not found")

        active = self.borrow_repo.find_active_borrow(user.id, book.isbn)
        if not active:
            raise ValueError("User did not borrow this book")

        if not book.return_copy():
            raise ValueError("Failed to return book")
        self.book_repo.update(book)

        active.return_date = datetime.now(timezone.utc)
        if not self.borrow_repo.update(active):
            raise ValueError("Failed to update borrow record")

    def search_book(self, book_title: str) -> str:
        books = self.book_repo.search_by_title(book_title)
        for b in books:
            if b.title.lower() == book_title.lower():
                if b.available_copies > 0:
                    return f"{book_title} is available"
                else:
                    return f"{book_title} is borrowed"
        return f"{book_title} is not available"


    def display_borrowed_books(self):
        users = self.user_repo.get_all()
        has_borrowed = False
        for user in users:
            borrowed_records = self.borrow_repo.get_borrowed_by_user(user.id)
            if borrowed_records:
                has_borrowed = True
                print(f"({user.username}):")
                for rec in borrowed_records:
                    print(f"  {rec.book.title}")
        if not has_borrowed:
            print("No books are currently borrowed")

    def get_all_books(self):
        books = self.book_repo.get_all()
        if books:
            print("\nAll Books in Library:")
            for book in books:
                status = f"Available: {book.available_copies}/{book.total_copies}"
                print(f"  ISBN: {book.isbn}, Title: {book.title}, Status: {status}")
        else:
            print("No books in library")

    def get_all_users(self):
        users = self.user_repo.get_all()
        if users:
            for user in users:
                borrowed_count = len(self.borrow_repo.get_borrowed_by_user(user.id))
                print(f"  ID: {user.id}, Name: {user.name}, Username: {user.username}, Books Borrowed: {borrowed_count}")
        else:
            print("No user registered")

    def search_books_by_title(self, title: str) -> List[Book]:
        return self.book_repo.search_by_title(title)

    def search_books_by_author(self, author: str) -> List[Book]:
        return self.book_repo.search_by_author(author)

    def search_books_by_category(self, category: str) -> List[Book]:
        return self.book_repo.search_by_category(category)

    def search_book_by_isbn(self, isbn: str) -> Optional[Book]:
        return self.book_repo.get_by_isbn(isbn)

    def delete_book(self, isbn: str):
        book = self.book_repo.get_by_isbn(isbn)
        if not book:
            raise ValueError("Book not found")
        # Check if any copies are borrowed
        if book.borrowed_copies > 0:
            raise ValueError(f"Cannot delete book: {book.borrowed_copies} copy(ies) are currently borrowed")
        if not self.book_repo.delete(book):
            raise ValueError("Failed to delete book")

    def delete_user(self, username: str):
        user = self.user_repo.get_by_username(username)
        if not user:
            raise ValueError("User not found")
        # Check if user has any active borrows
        active_borrows = self.borrow_repo.get_borrowed_by_user(user.id)
        if active_borrows:
            raise ValueError(f"Cannot delete user: has {len(active_borrows)} borrowed book(s) not returned")
        if not self.user_repo.delete(user):
            raise ValueError("Failed to delete user")


            