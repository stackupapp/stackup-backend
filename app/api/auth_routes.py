from fastapi import APIRouter
from app.api.auth import router as auth_router
from app.api.upload_routes import router as upload_router
from app.api.portfolio_routes import router as portfolio_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(upload_router)
router.include_router(portfolio_router)