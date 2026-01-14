
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.video import Video
from src.schemas.video import CreateVideoPayload, ListVideoPayload, ListVideoResponse, UpdateVideoPayload, VideoBase
from src.core.database import get_async_session


class VideoService:
    def __init__(
        self,
        session: AsyncSession = Depends(get_async_session)
    ):
        self._session = session

    async def create_video(self, video: CreateVideoPayload):
        new_video = Video(**video.model_dump())
        self._session.add(new_video)
        await self._session.commit()
        await self._session.refresh(new_video)
        return new_video

    async def get_videos(self, data: ListVideoPayload):

        stmt = (
            select(Video)
        )

        filters = {
            "status": lambda stmt, value: (
                stmt
                .where(Video.status.in_(value))
            ),
            "camera_number": lambda stmt, value: (
                stmt
                .where(Video.camera_number.in_(value))
            ),
            "location": lambda stmt, value: (
                stmt
                .where(Video.location.in_(value))
            ),
            "start_time_from": lambda stmt, value: (
                stmt
                .where(Video.start_time >= value)
            ),
            "start_time_to": lambda stmt, value: (
                stmt
                .where(Video.start_time <= value)
            ),
        }

        for key, value in data:
            if value is None:
                continue
            filter_func = filters.get(key)
            if filter_func is None:
                continue
            stmt = filter_func(stmt, value)

        result = (await self._session.execute(stmt)).unique().scalars().all()
        videos_list = [VideoBase.model_validate(video) for video in result]
        return ListVideoResponse(videos=videos_list)

    async def get_video(self, video_id: int):
        stmt = select(Video).where(Video.id == video_id)
        result = (await self._session.execute(stmt)).unique().scalars().one()
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")
        return result

    async def update_video(self, video_id: int, video: UpdateVideoPayload):
        stmt = select(Video).where(Video.id == video_id)
        result = (await self._session.execute(stmt)).unique().scalars().one()
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")
        result.status = video.status
        await self._session.commit()
        await self._session.refresh(result)
        return result