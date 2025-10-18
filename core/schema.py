import strawberry
from .type import CharacterType, FilmType, PlanetType
from .models import Character, Film, Planet

@strawberry.type
class Query:
    Character: list[CharacterType] = strawberry.field(
        resolver=lambda: Character.objects.all()
    )
    
    films: list[FilmType] = strawberry.field(
        resolver=lambda: Film.objects.all())
    
    planets: list[PlanetType] = strawberry.field(
        resolver=lambda: Planet.objects.all()
    )

shchema = strawberry.Schema(query=Query)