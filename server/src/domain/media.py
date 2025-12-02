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


class MediaRating(Enum):
    TERRIBLE = 1
    VERY_BAD = 2
    BAD = 3
    POOR = 4
    AVERAGE = 5
    FINE = 6
    GOOD = 7
    VERY_GOOD = 8
    GREAT = 9
    MASTERPIECE = 10


@dataclass
class Media:
    """Domain representation of a media."""

    title: str
    user_id: int
    status: Optional[MediaStatus] = None
    _rating: Optional[MediaRating] = None
    mediaType: Optional[MediaType] = None
    description: Optional[str] = None
    id: Optional[int] = None

    def __str__(self):
        return self.title

    @property
    def rating(self):
        return self._rating.value if self._rating else None

    @rating.setter
    def rating(self, value):
        if value is None:
            self._rating = None
        elif isinstance(value, int) and 1 <= value <= 10:
            self._rating = MediaRating(value)
        else:
            raise ValueError("Rating must be between 1 and 10 or None")
