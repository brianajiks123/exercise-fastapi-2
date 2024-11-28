from fastapi import FastAPI, HTTPException, Path, Query, Depends
from sqlmodel import Session, select
from model.models import GenreURLChoices, CreateBand, Band, Album
from typing import Annotated
from model.db import get_session

app = FastAPI()

@app.get("/bands")
async def bands(
        genre: GenreURLChoices | None = None,
        q: Annotated[str | None, Query(max_length=10)] = None,
        session: Session = Depends(get_session)
    ) -> list[Band]:
    band_list = session.exec(select(Band)).all()
    
    if genre:
        band_list = [band for band in band_list if band.genre.value.lower() == genre.value]
    
    if q:
        band_list = [band for band in band_list if q.lower() in band.name.lower()]
    
    return band_list

@app.post("/bands")
async def create_band(
        band_data: CreateBand,
        session: Session = Depends(get_session)
    ) -> Band:
    band = Band(name=band_data.name, genre=band_data.genre)
    session.add(band)
    
    if band_data.albums:
        for album in band_data.albums:
            album_obj = Album(title=album.title, release_date=album.release_date, band=band)
            session.add(album_obj)
    
    session.commit()
    session.refresh(band)
    return band

@app.get("/bands/{band_id}")
async def band(
        band_id: Annotated[int, Path(title="The band ID")],
        session: Session = Depends(get_session)
    ) -> Band:
    band = session.get(Band, band_id)
    
    if band is None:
        # status code 404
        raise HTTPException(status_code=404, details='Band not found')
    
    return band
