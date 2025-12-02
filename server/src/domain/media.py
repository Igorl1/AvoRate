from dataclasses import dataclass
from typing import Optional
from enum import Enum


class MediaStatus(Enum):
    CONSUMING = "consuming"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    DROPPED = "dropped"
    PLANNED = "planned"


class MediaType(Enum):
    MOVIE = "movie"
    BOOK = "book"
    GAME = "game"
    SERIES = "series"
    ANIME = "anime"
    MANGA = "manga"
    TV_SHOW = "tv_show"
    PODCAST = "podcast"
    OTHER = "other"


@dataclass
class Media:
    """Domain representation of a media."""

    # TODO: Add user association after login logic
    title: str
    status: Optional[MediaStatus] = None
    _rating: Optional[int] = None
    mediaType: Optional[MediaType] = None
    description: Optional[str] = None

    def __str__(self):
        return self.title

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if value <= 10 and value >= 0:
            self._rating = value
        else:
            raise ValueError("Rating must be between 0 and 10")
