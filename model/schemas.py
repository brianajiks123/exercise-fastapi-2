from datetime import date
from enum import Enum
from pydantic import BaseModel, validator

class GenreURLChoices(Enum):
    ROCK = 'rock'
    POP = 'pop'

class GenreChoices(Enum):
    ROCK = 'Rock'
    POP = 'Pop'

class Album(BaseModel):
    title: str
    release_date: date

class BandBase(BaseModel):
    name: str
    genre: GenreChoices
    albums: list[Album] = []     # default value is empty list, None is null

class CreateBand(BandBase):
    @validator('genre', pre=True)
    def title_case_genre(cls, value):
        return value.title()

class BandWithID(BandBase):
    id: int
