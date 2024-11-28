from datetime import date
from enum import Enum
from pydantic import validator
from sqlmodel import SQLModel, Field, Relationship

class GenreURLChoices(Enum):
    ROCK = 'rock'
    POP = 'pop'

class GenreChoices(Enum):
    ROCK = 'Rock'
    POP = 'Pop'

class BandBase(SQLModel):
    name: str
    genre: GenreChoices

class Band(BandBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    albums: list["Album"] = Relationship(back_populates="band")

class AlbumBase(SQLModel):
    title: str
    release_date: date
    band_id: int | None = Field(default=None, foreign_key="band.id")         # Belongs to Band

class Album(AlbumBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    band: Band | None = Relationship(back_populates="albums")

class CreateBand(BandBase):
    albums: list[AlbumBase] | None = None       # Optional Field

    @validator('genre', pre=True)
    def title_case_genre(cls, value):
        return value.title()
