from sqlalchemy import TIMESTAMP, CheckConstraint, DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from src.core.database import Base
from src.schemas.video import VideoStatus


class Video(Base):
    __tablename__ = 'videos'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    video_path: Mapped[str] = mapped_column(nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    duration: Mapped[int] = mapped_column(nullable=False)
    camera_number: Mapped[int] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[VideoStatus] = mapped_column(default=VideoStatus.NEW)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.current_timestamp(),
    )

    __table_args__ = (
        CheckConstraint('duration > 0', name='duration_positive'),
    )
