from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from persistence.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)   # external user_id
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    