from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.user import UserRegister, UserLogin, TokenResponse
from app.services.auth import AuthService


router=APIRouter(prefix="/auth",tags=["Auth"])

@router.post("/register",response_model=TokenResponse)
async def register(data: UserRegister, db: AsyncSession=Depends(get_db):
    service=AuthService(db)
    return await service.register(data)

@router.post("/login",response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession=Depends(get_db)):
    service=AuthService(db)
    return await service.login(data)