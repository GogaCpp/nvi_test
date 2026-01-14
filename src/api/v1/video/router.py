from typing import Annotated
from fastapi import APIRouter, Depends, Query

from src.services.video import VideoService
from src.schemas.video import (
    CreateVideoPayload, CreateVideoResponse, GetVideoResponse,
    ListVideoPayload, ListVideoResponse, UpdateVideoPayload, UpdateVideoResponse
)


router = APIRouter(prefix="/videos", tags=["Videos"])


@router.post("/", response_model=CreateVideoResponse)
async def create_video(
    video: CreateVideoPayload,
    service: VideoService = Depends(),
):
    return await service.create_video(video)


@router.get("/", response_model=ListVideoResponse)
async def get_videos(
    filters: Annotated[ListVideoPayload, Query()],
    service: VideoService = Depends(),
):
    return await service.get_videos(filters)


@router.get("/{video_id}", response_model=GetVideoResponse)
async def get_video(
    video_id: int,
    service: VideoService = Depends(),
):
    return await service.get_video(video_id)


@router.patch("/{video_id}/status", response_model=UpdateVideoResponse)
async def update_video(
    video_id: int,
    video: UpdateVideoPayload,
    service: VideoService = Depends(),
):
    return await service.update_video(video_id, video)
