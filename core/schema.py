import strawberry
from .type import CharacterType, FilmType, PlanetType
from .models import Character, Film, Planet
from core.mutations import Mutation

@strawberry.type
class Query:
    Character: list[CharacterType] = strawberry.field(
        resolver=lambda: Character.objects.all()
    )
    @strawberry.field
    def character_by_name(self, name: str) -> CharacterType | None:
        try:
            return Character.objects.get(name__iexact=name)
        except Character.DoesNotExist:
            return None
        
    films: list[FilmType] = strawberry.field(
        resolver=lambda: Film.objects.all())
    
    planets: list[PlanetType] = strawberry.field(
        resolver=lambda: Planet.objects.all()
    )

shchema =  strawberry.Schema(query=Query, mutation=Mutation)