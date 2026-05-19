from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import Session
from persistence.decorator import with_session
from models.user import User

class UserRepository:
    @with_session
    def create(self, user: User, session: Session = None) -> bool:
        try:
            session.add(user)
            session.flush()
            return True
        except Exception:
            return False

    @with_session
    def get_by_id(self, user_id: str, session: Session = None) -> Optional[User]:
        return session.get(User, user_id)

    @with_session
    def get_by_username(self, username: str, session: Session = None) -> Optional[User]:
        stmt = select(User).where(User.username == username)
        return session.scalar(stmt)

    @with_session
    def get_all(self, session: Session = None) -> List[User]:
        stmt = select(User)
        return list(session.scalars(stmt).all())
    
    @with_session
    def delete(self, user: User, session: Session = None) -> bool:
        try:
            session.delete(user)
            session.flush()
            return True
        except Exception:
            return False