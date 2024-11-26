from fastapi import FastAPI, HTTPException
from model.schemas import GenreURLChoices, BandBase, CreateBand, BandWithID

app = FastAPI()

BANDS = [
    {'id': 1, 'name': "Brian", 'genre': 'Rock', 'albums': [
        {'title': 'Master of Hell', 'release_date': '2020-02-05'}
    ]},
    {'id': 2, 'name': "Aji", 'genre': 'Pop'},
    {'id': 3, 'name': "Pamungkas", 'genre': 'Rock'},
]

@app.get("/")
async def home():       # by default return dict[str,str]
    return {"msg": "hello1!"}

@app.get("/about")
async def about():      # by default return str
    return 'An Exceptional Company.'

# @app.get("/bands")
# async def bands():      # by default return list[dict]
#     return BANDS

# @app.get("/bands")
# async def bands() -> list[Band]:      # return list of Band object
#     return [Band(**band) for band in BANDS]

@app.get("/bands")
async def bands(
        genre: GenreURLChoices | None = None,
        has_albums: bool = False
    ) -> list[BandWithID]:      # return list of Band object with optional genre params
    band_list = [BandWithID(**band) for band in BANDS]
    
    if genre:
        band_list = [band for band in band_list if band.genre.value.lower() == genre.value]
    
    if has_albums:
        band_list = [band for band in band_list if len(band.albums) > 0]
    return band_list

@app.post("/bands")
async def create_band(band_data: CreateBand) -> BandWithID:       # return to generate band ID with band data
    id_band = BANDS[-1]['id'] + 1
    band = BandWithID(id=id_band, **band_data.model_dump()).model_dump()
    BANDS.append(band)
    return band

# @app.get("/bands/{band_id}")
# async def band(band_id: int):      # by default return dict, type-hint: integer for params
#     band = next((band for band in BANDS if band['id'] == band_id), None)
#     if band is None:
#         # status code 404
#         raise HTTPException(status_code=404, details='Band not found')
#     return band

@app.get("/bands/{band_id}")
async def band(band_id: int) -> BandWithID:      # return Band object, type-hint: integer for params
    band = next((BandWithID(**band) for band in BANDS if band['id'] == band_id), None)
    if band is None:
        # status code 404
        raise HTTPException(status_code=404, details='Band not found')
    return band

# @app.get("/bands/{band_id}", status_code=206)       # change status_code for success response
# async def band(band_id: int):      # by default return dict, type-hint: integer for params
#     band = next((band for band in BANDS if band['id'] == band_id), None)
#     if band is None:
#         # status code 404
#         raise HTTPException(status_code=404, details='Band not found')
#     return band

# @app.get("/bands/genre/{genre}")
# async def bands_for_genre(genre: str) -> list[dict]:      # return list of dict, type-hint: string for params
#     return [band for band in BANDS if band['genre'].lower() == genre.lower()]       # lower case to validation params

@app.get("/bands/genre/{genre}")
async def bands_for_genre(genre: GenreURLChoices) -> list[dict]:      # return list of dict, type-hint: enum for params
    return [band for band in BANDS if band['genre'].lower() == genre.value]       # lower case to validation params with value of enum
