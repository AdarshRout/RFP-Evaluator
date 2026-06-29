from fastapi import APIRouter
from app.api.v1.routes import evaluation, health

router = APIRouter(prefix="/api/v1")
router.include_router(health.router)
router.include_router(evaluation.router)
