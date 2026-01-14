from fastapi import APIRouter

from .video import router as video_router


router = APIRouter(prefix="/v1")
router.include_router(video_router)
