import pytest
from asgiref.sync import async_to_sync
from core.models import Character, Planet, Film
from core.schema import shchema

@pytest.mark.django_db
def test_characters_query():
    # Crear datos de prueba
    planet = Planet.objects.create(name="Tatooine", climate="Arid", terrain="Desert")
    Character.objects.create(name="Luke Skywalker", height="172", mass="77", gender="male", homeworld=planet)
    Character.objects.create(name="Leia Organa", height="150", mass="49", gender="female", homeworld=planet)

    query = """
        query {
            characters {
                edges {
                    node {
                        name
                        height
                        gender
                    }
                }
            }
        }
    """

    # Ejecutar la consulta async desde contexto síncrono
    result = async_to_sync(shchema.execute)(query)

    assert result.errors is None
    assert result.data == {
        "characters": {
            "edges": [
                {"node": {"name": "Luke Skywalker", "height": "172", "gender": "male"}},
                {"node": {"name": "Leia Organa", "height": "150", "gender": "female"}},
            ]
        }
    }

@pytest.mark.django_db
def test_search_characters_query():
    # Crear datos de prueba
    planet = Planet.objects.create(name="Alderaan", climate="Temperate", terrain="Grasslands")
    Character.objects.create(name="Luke Skywalker", height="172", gender="male", homeworld=planet)
    Character.objects.create(name="Leia Organa", height="150", gender="female", homeworld=planet)

    query = """
        query SearchCharacters($name: String) {
            searchCharacters(name: $name) {
                edges {
                    node {
                        name
                        gender
                    }
                }
            }
        }
    """

    # Ejecutar consulta async desde contexto síncrono
    result = async_to_sync(shchema.execute)(query, variable_values={"name": "Leia"})

    assert result.errors is None
    assert result.data == {
        "searchCharacters": {
            "edges": [
                {"node": {"name": "Leia Organa", "gender": "female"}}
            ]
        }
    }

@pytest.mark.django_db
def test_create_character_mutation():
    planet = Planet.objects.create(name="Tatooine")
    film1 = Film.objects.create(title="A New Hope", episode_id=4, release_date="1977-05-25")
    film2 = Film.objects.create(title="The Empire Strikes Back", episode_id=5, release_date="1980-05-21")

    mutation = """
        mutation CreateCharacter($name: String!, $height: String, $gender: String, $filmsIds: [Int!]) {
    createCharacter(name: $name, height: $height, gender: $gender, filmsIds: $filmsIds) {
                name
                height
                gender
                films {
                    id
                    title
                }
            }
        }
    """

    result = shchema.execute_sync(
    mutation,
    variable_values={
        "name": "Han Solo",
        "height": "180",
        "gender": "male",
        "filmsIds": [film1.id, film2.id]
    }
)

    assert result.errors is None
    assert result.data == {
    "createCharacter": {
        "name": "Han Solo",
        "height": "180",
        "gender": "male",
        "films": [
            {"id": str(film1.id), "title": "A New Hope"},
            {"id": str(film2.id), "title": "The Empire Strikes Back"}
        ]
    }
}

    # Ejecutar mutation de forma síncrona
    result = shchema.execute_sync(
        mutation,
        variable_values={
            "name": "Han Solo",
            "height": "180",
            "gender": "male",
            "filmsIds": [film1.id, film2.id]
        }
    )

    assert result.errors is None
    assert result.data == {
    "createCharacter": {
        "name": "Han Solo",
        "height": "180",
        "gender": "male",
        "films": [
            {"id": str(film1.id), "title": "A New Hope"},
            {"id": str(film2.id), "title": "The Empire Strikes Back"}
        ]
    }
}


@pytest.mark.django_db
def test_create_planet_mutation():
    mutation = """
        mutation CreatePlanet($name: String!, $climate: String, $terrain: String, $population: String) {
            createPlanet(name: $name, climate: $climate, terrain: $terrain, population: $population) {
                name
                climate
                terrain
                population
            }
        }
    """

    result = shchema.execute_sync(
        mutation,
        variable_values={
            "name": "Dagobah",
            "climate": "Swampy",
            "terrain": "Swamp",
            "population": "Unknown"
        }
    )

    assert result.errors is None
    assert result.data == {
        "createPlanet": {
            "name": "Dagobah",
            "climate": "Swampy",
            "terrain": "Swamp",
            "population": "Unknown"
        }
    }

@pytest.mark.django_db
def test_create_film_mutation():
    # Crear un planeta para asociarlo opcionalmente
    planet = Planet.objects.create(name="Endor", climate="Temperate", terrain="Forest")

    mutation = """
        mutation CreateFilm($title: String!, $episodeId: Int!, $releaseDate: String!, $planetsIds: [Int!]) {
            createFilm(
                title: $title,
                episodeId: $episodeId,
                releaseDate: $releaseDate,
                planetsIds: $planetsIds
            ) {
                title
                episodeId
                releaseDate
                planets {
                    id
                    name
                }
            }
        }
    """

    result = shchema.execute_sync(
        mutation,
        variable_values={
            "title": "Return of the Jedi",
            "episodeId": 6,
            "releaseDate": "1983-05-25",
            "planetsIds": [planet.id]
        }
    )

    assert result.errors is None
    assert result.data == {
        "createFilm": {
            "title": "Return of the Jedi",
            "episodeId": 6,
            "releaseDate": "1983-05-25",
            "planets": [
                {"id": str(planet.id), "name": "Endor"}
            ]
        }
    }