from typing import Optional, List
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from persistence.decorator import with_session
from models.book import Book

class BookRepository:
    @with_session
    def create(self, book: Book, session: Session = None) -> bool:
        try:
            session.add(book)
            session.flush()
            return True
        except Exception:
            return False

    # @with_session
    # def get_by_id(self, book_id: str, session: Session = None) -> Optional[Book]:
    #     return session.get(Book, book_id)

    @with_session
    def search_by_title(self, title: str, session: Session = None) -> List[Book]:
        stmt = select(Book).where(Book.title.ilike(f"%{title}%"))
        return list(session.scalars(stmt).all())

    @with_session
    def book_exists(self, isbn: str, session: Session = None) -> bool:
        return self.get_by_isbn(isbn) is not None
    
    # @with_session
    # def book_exists(self, isbn: str, session: Session = None) -> bool:
    #     if self.get_by_isbn(isbn):
    #         return True
    #     else:
    #         return False


    @with_session
    def update(self, book: Book, session: Session = None) -> bool:
        try:
            session.merge(book)
            session.flush()
            return True
        except Exception:
            return False

    @with_session
    def get_all(self, session: Session = None) -> List[Book]:
        stmt = select(Book).order_by(Book.title)
        return session.scalars(stmt).all()

    @with_session
    def search_by_author(self, author: str, session: Session = None) -> List[Book]:
        stmt = select(Book).where(Book.author.ilike(f"%{author}%"))
        return session.scalars(stmt).all()

    @with_session
    def search_by_category(self, category: str, session: Session = None) -> List[Book]:
        stmt = select(Book).where(Book.category.ilike(f"%{category}%"))
        return session.scalars(stmt).all()

    @with_session
    def get_by_isbn(self, isbn: str, session: Session = None) -> Optional[Book]:
        return session.get(Book, isbn)
    
    @with_session
    def delete(self, book: Book, session: Session = None) -> bool:
        try:
            session.delete(book)
            session.flush()
            return True
        except Exception:
            return False