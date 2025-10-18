import strawberry
from core.models import Character, Film, Planet
from core.type import CharacterType, FilmType, PlanetType

@strawberry.type
class Mutation:
    @strawberry.mutation
    def update_character_name(self, id: int, new_name: str) -> CharacterType | None:
        try:
            char = Character.objects.get(id=id)
            char.name = new_name
            char.save()
            return char
        except Character.DoesNotExist:
            return None

    # Funciones para crear un nuevo personaje, planeta o pelicula
    @strawberry.mutation
    def create_character(
        self,
        name: str,
        height: str = "",
        mass: str = "",
        gender: str = "",
        films_ids: list[int] = strawberry.UNSET
    ) -> CharacterType:
        
        char = Character.objects.create(
            name=name,
            height=height,
            mass=mass,
            gender=gender,
        )

        if films_ids is not strawberry.UNSET:
            films = Film.objects.filter(id__in=films_ids)
            char.films.set(films)

        return char
    
    @strawberry.mutation
    def create_film(
        self,
        title: str,
        episode_id: int,
        opening_crawl: str = "",
        director: str = "",
        producer: str = "",
        release_date: str = "1970-01-01",
        desc: str = "",
        planets_ids: list[int] = strawberry.UNSET
    ) -> FilmType:
        
        film = Film.objects.create(
            title=title,
            episode_id=episode_id,
            opening_crawl=opening_crawl,
            director=director,
            producer=producer,
            release_date=release_date,
            desc=desc,
        )

        if planets_ids is not strawberry.UNSET:
            planets = Planet.objects.filter(id__in=planets_ids)
            film.planets.set(planets)

        return film
    
    @strawberry.mutation
    def create_planet(
        self,
        name: str,
        climate: str = "",
        terrain: str = "",
        population: str = ""
    ) -> PlanetType:
        
        planet = Planet.objects.create(
            name=name,
            climate=climate,
            terrain=terrain,
            population=population,
        )

        return planet