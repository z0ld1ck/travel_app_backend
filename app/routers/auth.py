from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.user import UserRegister, UserLogin, TokenResponse
from app.services.auth import AuthService

<<<<<<< HEAD
router = APIRouter(prefix="/auth", tags=["Auth"])

# POST /auth/register
@router.post("/register", response_model=TokenResponse)
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    # Depends(get_db) — FastAPI автоматически создаёт
    # сессию БД и передаёт её в функцию
    service = AuthService(db)
    return await service.register(data)

# POST /auth/login
@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
=======

router=APIRouter(prefix="/auth",tags=["Auth"])

@router.post("/register",response_model=TokenResponse)
async def register(data: UserRegister, db: AsyncSession=Depends(get_db):
    service=AuthService(db)
    return await service.register(data)

@router.post("/login",response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession=Depends(get_db)):
    service=AuthService(db)
>>>>>>> 37b5bafc8839473980d31976cb119392abc83d47
    return await service.login(data)