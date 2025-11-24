from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Media:
     """Domain representation of a media."""

    ##COLOCAR USER APOS LOGICA DE LOGIN
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
        if value<=10 and value>=0:
            self._rating = value
        else:
            raise ValueError("Rating deve ser entre 0 e 10")

        

