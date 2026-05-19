from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from persistence.database import Base

class Book(Base):
    __tablename__ = "books"

    isbn: Mapped[str] = mapped_column(String(20), primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    total_copies: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    borrowed_copies: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    @property
    def available_copies(self) -> int:
        return self.total_copies - self.borrowed_copies

    def borrow_copy(self) -> bool:
        if self.available_copies > 0:
            self.borrowed_copies += 1
            return True
        return False

    def return_copy(self) -> bool:
        if self.borrowed_copies > 0:
            self.borrowed_copies -= 1
            return True
        return False


        