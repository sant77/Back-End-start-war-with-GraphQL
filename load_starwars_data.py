import os
import json
import django

# Configuración de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


from core.models import Planet, Film, Character  # ajusta el nombre del app si es distinto

cwd = os.getcwd()

# Ruta base donde están las carpetas
BASE_DIR = os.path.join(cwd, 'file_to_load')


def extract_id_from_url(url):
    """Extrae el número ID de una URL tipo http://swapi.co/api/planets/61/"""
    try:
        return int(url.strip("/").split("/")[-1])
    except Exception:
        return None


def load_json_data():
    """Carga los JSON en memoria y devuelve un diccionario."""
    data = {"films": [], "people": [], "planets": []}
    json_keys = ["film", "people", "planet"]

    for index, category in enumerate(data.keys()):
        folder_path = os.path.join(BASE_DIR, category)
        if not os.path.exists(folder_path):
            print(f"⚠️ No se encontró la carpeta: {folder_path}")
            continue

        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)
                file_id = int(filename.replace(".json", ""))  # ID = número del archivo
                with open(file_path, "r", encoding="utf-8") as f:
                    content = json.load(f)
                    key = json_keys[index]
                    if key in content:
                        item = content[key]
                        item["id"] = file_id
                        data[category].append(item)
    return data


def populate_database():
    data = load_json_data()

    print("🪐 Cargando planetas...")
    for planet in data["planets"]:
        if "name" not in planet:
            print(f"❌ Planeta sin nombre: {planet}")
            continue  # saltar este registro temporalmente
        Planet.objects.update_or_create(
            id=planet["id"],
            defaults={
                "name": planet["name"],
                "climate": planet.get("climate", ""),
                "terrain": planet.get("terrain", ""),
                "population": planet.get("population", ""),
            },
        )

    print("🎬 Cargando películas...")
    for film in data["films"]:
        Film.objects.update_or_create(
            id=film["id"],
            defaults={
                "title": film["title"],
                "episode_id": film["episode_id"],
                "opening_crawl": film.get("opening_crawl", ""),
                "director": film.get("director", ""),
                "producer": film.get("producer", ""),
                "release_date": film.get("release_date", "1970-01-01"),
                "desc": " ".join(film.get("desc", [])),
            },
        )

    print("👤 Cargando personajes...")
    for person in data["people"]:
        homeworld_id = extract_id_from_url(person.get("homeworld", ""))

        Character.objects.update_or_create(
            id=person["id"],
            defaults={
                "name": person["name"],
                "height": person.get("height"),
                "mass": person.get("mass"),
                "hair_color": person.get("hair_color"),
                "skin_color": person.get("skin_color"),
                "eye_color": person.get("eye_color"),
                "birth_year": person.get("birth_year"),
                "gender": person.get("gender"),
                "desc": " ".join(person.get("desc", [])),
                "homeworld_id": homeworld_id if homeworld_id else None,
            },
        )

    print("🔗 Estableciendo relaciones...")

    # Relaciones Film-Planet
    for film in data["films"]:
        film_obj = Film.objects.get(id=film["id"])
        for planet_url in film.get("planets", []):
            planet_id = extract_id_from_url(planet_url)
            if planet_id and Planet.objects.filter(id=planet_id).exists():
                film_obj.planets.add(planet_id)

    # Relaciones Character-Film
    for person in data["people"]:
        char_obj = Character.objects.get(id=person["id"])
        for film_url in person.get("films", []):
            film_id = extract_id_from_url(film_url)
            if film_id and Film.objects.filter(id=film_id).exists():
                char_obj.films.add(film_id)

    print("✅ Carga completa.")


if __name__ == "__main__":
    populate_database()
