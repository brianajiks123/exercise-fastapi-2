from fastapi import FastAPI, HTTPException
from enum import Enum

app = FastAPI()

class GenreURLChoices(Enum):
    ROCK = 'rock'
    ELECTRONIC = 'electronic'
    METAL = 'metal'
    HIP_HOP = 'hip-hop'

BANDS = [
    {'id': 1, 'name': "Brian", 'genre': 'Rock'},
    {'id': 2, 'name': "Aji  ", 'genre': 'Pop'},
    {'id': 3, 'name': "Pamungkas", 'genre': 'Rock'},
]

@app.get("/")
async def home():       # by default return dict[str,str]
    return {"msg": "hello1!"}

@app.get("/about")
async def about():      # by default return str
    return 'An Exceptional Company.'

@app.get("/bands")
async def bands():      # by default return list[dict]
    return BANDS

@app.get("/bands/{band_id}")
async def band(band_id: int):      # by default return dict, type-hint: integer for params
    band = next((band for band in BANDS if band['id'] == band_id), None)
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
#     return [
#         band for band in BANDS if band['genre'].lower() == genre.lower()    # lower case to validation params
#     ]

@app.get("/bands/genre/{genre}")
async def bands_for_genre(genre: GenreURLChoices) -> list[dict]:      # return list of dict, type-hint: enum for params
    return [
        band for band in BANDS if band['genre'].lower() == genre.value    # lower case to validation params with value of enum
    ]
