import strawberry_django
from strawberry import auto, relay
from . import models
import strawberry

@strawberry_django.type(models.Planet)
class PlanetType(relay.Node):
    id: auto
    name: auto
    climate: auto
    terrain: auto
    population: auto


@strawberry_django.type(models.Film)
class FilmType(relay.Node):
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
class CharacterType(relay.Node):
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

# Integración con Relay para paginación
@strawberry.type
class CharacterConnection(relay.Connection[CharacterType]):
    total_count: int

    @classmethod
    def resolve_connection(cls, nodes, info, **kwargs) -> "CharacterConnection":
        connection = super().resolve_connection(nodes, info, **kwargs)
        connection.total_count = len(nodes) if nodes else models.Character.objects.count()
        return connection