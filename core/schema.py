import strawberry
import strawberry_django
from strawberry_django.relay import DjangoListConnection
from .models import Character, Film, Planet
from .type import CharacterType, FilmType, PlanetType
from core.mutations import Mutation


@strawberry.type
class Query:

    # Lista completa de personajes con paginación estándar
    characters: DjangoListConnection[CharacterType] = strawberry_django.connection()

    # Ejemplo de búsqueda con Relay
    @strawberry_django.connection(DjangoListConnection[CharacterType])
    def search_characters(self, name: str | None = None) -> list[Character]:
        queryset = Character.objects.all()
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    # Films y planets también con Relay
    films: DjangoListConnection[FilmType] = strawberry_django.connection()
    planets: DjangoListConnection[PlanetType] = strawberry_django.connection()


shchema =  strawberry.Schema(query=Query, mutation=Mutation)