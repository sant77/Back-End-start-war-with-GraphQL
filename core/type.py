import strawberry_django
from strawberry import auto
from . import models

@strawberry_django.type(models.Planet)
class PlanetType:
    id: auto
    name: auto
    climate: auto
    terrain: auto
    population: auto

@strawberry_django.type(models.Film)
class FilmType:
    id: auto
    title: auto
    episode_id: auto
    opening_crawl: auto
    director: auto
    producer: auto
    release_date: auto
    desc: auto
    planets: list[PlanetType]

@strawberry_django.type(models.Character)
class CharacterType:
    id: auto
    name: auto
    height: auto
    mass: auto
    hair_color: auto
    skin_color: auto
    eye_color: auto
    birth_year: auto
    gender: auto
    homeworld: PlanetType
    films: list[FilmType]
    desc: auto