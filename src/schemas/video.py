from datetime import datetime
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class VideoStatus(StrEnum):
    NEW = "NEW"
    TRANSCODED = "TRANSCODED"
    RECOGNIZED = "RECOGNIZED"


class VideoBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)

    id: int
    video_path: str
    start_time: Optional[datetime] = None
    duration: int
    camera_number: int
    location: str
    status: VideoStatus
    created_at: datetime


class CreateVideoPayload(BaseModel):
    video_path: str
    start_time: datetime | None = None
    duration: int = Field(ge=0)
    camera_number: int
    location: str


class CreateVideoResponse(VideoBase):
    pass


class ListVideoPayload(BaseModel):
    status: list[VideoStatus] | None = None
    camera_number: list[int] | None = None
    location: list[str] | None = None
    start_time_from: datetime | None = None
    start_time_to: datetime | None = None


class ListVideoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)

    videos: list[VideoBase | None]


class UpdateVideoPayload(BaseModel):
    status: VideoStatus


class UpdateVideoResponse(VideoBase):
    pass


class GetVideoResponse(VideoBase):
    pass
