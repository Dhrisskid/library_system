from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from persistence.database import Base

class BorrowRecord(Base):
    __tablename__ = "borrow_records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(50), ForeignKey("users.id"))
    book_isbn: Mapped[str] = mapped_column(String(20), ForeignKey("books.isbn"))
    borrow_date: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    return_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    user = relationship("User")
    book = relationship("Book")


    