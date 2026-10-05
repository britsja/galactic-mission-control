# Galactic Mission Control

A Flask learning project that uses the Star Wars API (SWAPI) to explore characters and create fictional galactic missions.

The project was built to practice several core Python and backend development concepts together in one application rather than learning each concept in isolation.

## Features

- Flask application with Blueprints
- REST-style GET and POST endpoints
- External SWAPI integration
- Pydantic models and validation
- Python type hints
- Custom execution-time decorator
- Dictionary comprehensions
- Dictionary unpacking
- Generators and `yield`
- Async HTTP requests with `asyncio` and HTTPX
- Concurrent API requests with `asyncio.gather()`
- HTML/CSS frontend
- JavaScript Fetch API
- Mission creation system
- API error handling
- Custom Pydantic validators

## Technologies

- Python 3
- Flask
- Pydantic
- HTTPX
- Requests
- asyncio
- HTML
- CSS
- JavaScript
- SWAPI

## Installation

### 1. Clone the repository

    git clone <repository-url>
    cd galactic-mission-control

Replace `<repository-url>` with the URL of your GitHub repository.

### 2. Create a virtual environment

On macOS/Linux:

    python3 -m venv .venv
    source .venv/bin/activate

On Windows:

    python -m venv .venv
    .venv\Scripts\activate

### 3. Install dependencies

    pip install -r requirements.txt

### 4. Run the application

    python app.py

The Flask development server should start on:

    http://127.0.0.1:5000

Open that address in your browser to access the Galactic Mission Control dashboard.

---

# API

The application provides several API endpoints that can also be accessed directly using cURL.

## Get a Character

Retrieve a Star Wars character by their SWAPI ID.

Endpoint:

    GET /api/v1/characters/<character_id>

Example:

    curl http://127.0.0.1:5000/api/v1/characters/1

Example response:

    {
        "birth_year": "19BBY",
        "character_id": 1,
        "height": "172",
        "homeworld": "https://swapi.info/api/planets/1",
        "mass": "77",
        "name": "Luke Skywalker",
        "profile": {
            "eye_color": "blue",
            "gender": "male",
            "hair_color": "blond",
            "skin_color": "fair"
        },
        "source": "SWAPI"
    }

## Get a Crew

Retrieve the predefined crew using concurrent asynchronous API requests.

Endpoint:

    GET /api/v1/characters/crew

Example:

    curl http://127.0.0.1:5000/api/v1/characters/crew

This endpoint demonstrates the use of `asyncio`, HTTPX and concurrent external API requests.

## Create a Mission

Create a fictional galactic mission.

Endpoint:

    POST /api/v1/missions

Example:

    curl -X POST http://127.0.0.1:5000/api/v1/missions \
      -H "Content-Type: application/json" \
      -d '{
        "mission_name": "Operation Twin Suns",
        "character_ids": [1, 5, 13],
        "planet_id": 1
      }'

Example response:

    {
        "crew": [
            {
                "character_id": 1,
                "name": "Luke Skywalker"
            },
            {
                "character_id": 5,
                "name": "Leia Organa"
            },
            {
                "character_id": 13,
                "name": "Chewbacca"
            }
        ],
        "crew_size": 3,
        "destination": "Tatooine",
        "mission_name": "Operation Twin Suns",
        "status": "MISSION READY"
    }

A successfully created mission returns:

    HTTP 201 Created

---

# Mission Validation

Mission requests are validated using Pydantic.

A mission requires:

- A mission name between 3 and 100 characters
- Between 1 and 6 crew members
- Positive SWAPI character IDs
- Unique character IDs
- A positive planet ID

For example, this request is invalid:

    {
        "mission_name": "X",
        "character_ids": [1, 1, -5],
        "planet_id": 0
    }

Pydantic rejects the request before the mission service or SWAPI requests are executed.

---

# Project Structure

    galactic-mission-control/
    │
    ├── app.py
    ├── requirements.txt
    ├── README.md
    │
    ├── models/
    │   ├── __init__.py
    │   ├── character.py
    │   └── mission.py
    │
    ├── routes/
    │   ├── __init__.py
    │   ├── characters.py
    │   └── missions.py
    │
    ├── services/
    │   ├── __init__.py
    │   ├── missions.py
    │   └── swapi.py
    │
    ├── utils/
    │   ├── __init__.py
    │   └── decorators.py
    │
    ├── templates/
    │   └── index.html
    │
    └── static/
        ├── css/
        │   └── style.css
        │
        └── js/
            └── app.js

## Directory Responsibilities

### `models/`

Contains Pydantic models that define and validate application data.

Examples include:

- `Character`
- `MissionRequest`

### `routes/`

Contains Flask Blueprints and HTTP endpoints.

The routes are responsible for receiving requests and returning HTTP responses.

### `services/`

Contains the application's business logic and external API communication.

`swapi.py` handles communication with SWAPI.

`missions.py` handles assembling mission data.

### `utils/`

Contains reusable utility functionality such as the custom execution-time decorator.

### `templates/`

Contains Flask/Jinja HTML templates.

### `static/`

Contains frontend CSS and JavaScript.

---

# Python Concepts Practiced

## Type Hinting

Functions use Python type hints to describe their expected inputs and outputs.

Example:

    def get_character(character_id: int) -> Character:

Async functions also use type hints:

    async def get_crew_async(
        client: httpx.AsyncClient,
        character_ids: list[int],
    ) -> list[Character]:

## Pydantic

Pydantic validates both external API data and incoming mission requests.

Example:

    character = Character(**data)

Dictionary unpacking passes the SWAPI response into the Pydantic model.

Mission requests are similarly validated with:

    mission_request = MissionRequest(**data)

## Dictionary Unpacking

Dictionary unpacking is used when constructing character summaries:

    summary = {
        **basic_info,
        "character_id": character_id,
        "profile": profile,
        "source": "SWAPI",
    }

It is also used when passing dictionaries as keyword arguments:

    Character(**data)

## Dictionary Comprehensions

Character data is filtered using dictionary comprehensions.

Example:

    basic_info = {
        key: value
        for key, value in character_data.items()
        if key in basic_fields
    }

## Custom Decorator

A custom decorator measures how long functions take to execute.

Example:

    @log_execution_time
    def get_character(character_id: int) -> Character:
        ...

The decorator demonstrates how Python functions can be wrapped with reusable behavior.

## Generators and `yield`

The project contains a crew generator:

    def generate_crew(character_ids):
        for character_id in character_ids:
            character = get_character(character_id)
            yield character

Unlike `return`, `yield` pauses the function and allows it to continue later.

This demonstrates lazy iteration.

## Asyncio

External API requests can be performed asynchronously.

Example:

    async def get_character_async(...):
        response = await client.get(url)

Multiple requests are executed concurrently using:

    characters = await asyncio.gather(*tasks)

This demonstrates how asynchronous programming can improve efficiency when a program spends time waiting for network I/O.

---

# Application Flow

A mission created from the browser follows this general flow:

    Browser
       |
       | JavaScript fetch()
       v
    Flask Route
       |
       v
    request.get_json()
       |
       v
    Python Dictionary
       |
       | **data
       v
    Pydantic MissionRequest
       |
       v
    Mission Service
       |
       v
    asyncio
       |
       +---- Character requests
       |
       +---- Planet request
       |
       v
    SWAPI
       |
       v
    Character Models
       |
       v
    Character Summaries
       |
       v
    Mission Dictionary
       |
       v
    Flask jsonify()
       |
       v
    HTTP Response
       |
       v
    JavaScript
       |
       v
    Browser Interface

---

# Frontend

The homepage provides two primary tools.

## Character Intelligence

Enter a SWAPI character ID to retrieve information about that character.

The browser makes a request to:

    /api/v1/characters/<character_id>

The returned JSON is then displayed on the page using JavaScript.

## Mission Creation

The mission interface accepts:

- Mission name
- Crew character IDs
- Destination planet ID

JavaScript converts the form data into JSON and sends it to:

    POST /api/v1/missions

The Flask backend validates the request, retrieves the required information from SWAPI and returns the assembled mission.

---

# Learning Purpose

This project is intended for learning and experimentation rather than production use.

The primary goal is to demonstrate how individual Python concepts can work together inside a small but functional web application.

Concepts covered include:

- Python functions
- Type hints
- Decorators
- Pydantic
- Validation
- Dictionaries
- Dictionary comprehensions
- Dictionary unpacking
- Lists
- Generators
- `yield`
- Async functions
- `await`
- `asyncio`
- Concurrent requests
- External APIs
- Flask routes
- Flask Blueprints
- GET requests
- POST requests
- JSON
- HTTP status codes
- Error handling
- JavaScript `fetch()`
- Frontend-to-backend communication

## Disclaimer

This application is a learning project and is not intended to be a production-ready system.

Star Wars data is retrieved from SWAPI.