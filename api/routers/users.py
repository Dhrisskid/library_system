from fastapi import APIRouter, HTTPException
from typing import List
from services.library_service import LibraryService
from api.schemas import UserCreate, UserOut

router = APIRouter(prefix="/users", tags=["users"])
service = LibraryService()

@router.post("", response_model=UserOut)
def register_user(payload: UserCreate):
    try:
        service.register_user(payload.user_id, payload.name, payload.username)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return service.user_repo.get_by_id(payload.user_id)

@router.get("", response_model=List[UserOut])
def list_users():
    return service.user_repo.get_all()

@router.delete("/{username}")
def delete_user(username: str):
    try:
        service.delete_user(username)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"detail": "User deleted successfully"}

    