# Documentación Técnica - API GraphQL Star Wars
## 1. Descripción del Proyecto

El proyecto consiste en una API GraphQL desarrollada en Django para un sitio dirigido a fanáticos de Star Wars. Permite consultar información de personajes, películas y planetas, así como crear nuevos registros mediante mutaciones. La base de datos utilizada es PostgreSQL y se encuentra dockerizada.

Funcionalidades principales

Listado de personajes con filtrado por nombre.

Consultar las películas en las que aparece cada personaje.

Consultar los planetas relacionados con cada película.

Crear nuevos personajes, películas y planetas mediante mutaciones.

Soporte de Relay para paginación y búsqueda avanzada.

Pruebas unitarias e integración.

##  2. Tecnologías utilizadas

- Python 3.12

- Django 5.2

- PostgreSQL

- Docker (para la base de datos)

- GraphQL con Strawberry

- Relay

- Pruebas: pytest

## 3. Estructura de carpetas
```bash
project_root/
│
├─ core/
│   ├─ models.py           # Modelos: Character, Film, Planet
│   ├─ type.py             # Tipos de GraphQL
│   ├─ schema.py           # Queries y Mutations de GraphQL
│   └─ mutations.py
│
├─ load_starwars_data.py  # Script para cargar datos automáticamente
│   
│
├─ settings/
│   ├─ settings.py
│   ├─ urls.py             # Configuración de GraphQL y admin
│
└─ tests/
    ├─ test_graphql.py
```
## 4. Base de Datos

PostgreSQL dockerizado.

URI de conexión en .env:

POSTGRES_URI=postgresql+psycopg2://starwars:starwars123@localhost:5432/starwars_db


Contiene tablas: character, film, planet y relaciones ManyToMany.


## 5. Configuración del .env
```bash
    POSTGRES_URI=
    # Base de datos
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    POSTGRES_DB=
    POSTGRES_HOST=
    POSTGRES_PORT=

    # Backend
    BACKEND_PORT=
```

## 6. Pruebas

Unitarias: se validan modelos y mutaciones.

Integración: se testean queries y mutaciones usando Postman o pytest.

Comando para correr tests:

```bash
pytest -v
```

## 7. Levantar el proyecto:

### Levantar ambiente virtual y correr 
```bash
    pip install -r requirements.txt
```

### Levanta contenedor
```bash
    docker-compose up -d postgres
```
### Correr migraciones

```bash
    python manage.py makemigrations
    python manage.py migrate
```

### Cargar datos automáticamente:
```bash
    python load_starwars_data.py
```

### Levantar servidor
```bash
    python manage.py runservery
```

### 8. Acceder a GraphiQL para documentación interactiva:

- http://localhost:8000/graphql/

### Nota si falla el create probablemente se requerra correr esto en las tablas:

```bash
    SELECT setval('core_planet_id_seq', (SELECT MAX(id) FROM  core_planet cp));

```