# from typing import Optional, List
# from sqlalchemy import select, and_
# from sqlalchemy.orm import Session, selectinload
# from persistence.decorator import with_session
# from models.borrow_record import BorrowRecord

# class BorrowRepository:
#     @with_session
#     def create(self, record: BorrowRecord, session: Session = None) -> bool:
#         try:
#             session.add(record)
#             session.flush()
#             return True
#         except Exception:
#             return False

#     @with_session
#     def find_active_borrow(self, user_id: str, book_isbn: str, session: Session = None) -> Optional[BorrowRecord]:
#         stmt = select(BorrowRecord).where(
#             and_(BorrowRecord.user_id == user_id,
#                 BorrowRecord.book_isbn == book_isbn,
#                 BorrowRecord.return_date.is_(None))
#         )
#         return session.scalar(stmt)


#     @with_session
#     def update(self, record: BorrowRecord, session: Session = None) -> bool:
#         try:
#             session.merge(record)
#             session.flush()
#             return True
#         except Exception:
#             return False




#     @with_session
#     def get_borrowed_by_user(self, user_id: str, session: Session = None):
#         stmt = select(BorrowRecord).where(
#             and_(BorrowRecord.user_id == user_id, BorrowRecord.return_date.is_(None))
#         ).options(selectinload(BorrowRecord.book))  # Eager load 'book'

from typing import Optional, List
from sqlalchemy import select, and_
from sqlalchemy.orm import Session, selectinload
from persistence.decorator import with_session
from models.borrow_record import BorrowRecord

class BorrowRepository:
    @with_session
    def create(self, record: BorrowRecord, session: Session = None) -> bool:
        try:
            session.add(record)
            session.flush()
            return True
        except Exception:
            return False

    @with_session
    def find_active_borrow(self, user_id: str, book_isbn: str, session: Session = None) -> Optional[BorrowRecord]:
        stmt = select(BorrowRecord).where(
            and_(BorrowRecord.user_id == user_id,
                 BorrowRecord.book_isbn == book_isbn,
                 BorrowRecord.return_date.is_(None))
        )
        return session.scalar(stmt)

    @with_session
    def update(self, record: BorrowRecord, session: Session = None) -> bool:
        try:
            session.merge(record)
            session.flush()
            return True
        except Exception:
            return False

    @with_session
    def get_borrowed_by_user(self, user_id: str, session: Session = None) -> List[BorrowRecord]:
        stmt = select(BorrowRecord).where(
            and_(BorrowRecord.user_id == user_id, BorrowRecord.return_date.is_(None))
        ).options(selectinload(BorrowRecord.book))   # Eager load the related book
        # .all() always returns a list (empty if no rows)
        return session.scalars(stmt).all()