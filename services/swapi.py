import requests
from models.character import Character
from utils.decorators import log_execution_time
from collections.abc import Generator
import asyncio
import httpx

BASE_URL: str = "https://swapi.info/api"

@log_execution_time
def get_character(character_id: int) -> Character:
  url: str = f"{BASE_URL}/people/{character_id}"
  response = requests.get(url, timeout=5)
  response.raise_for_status()
  data: dict = response.json()
  character = Character(**data)
  return character

def create_character_summary(
    character: Character,
    character_id: int,
) -> dict:
  character_data: dict = character.model_dump()

  basic_fields: list[str] = [
    "name",
    "height",
    "mass",
    "birth_year",
    "homeworld",
  ]

  basic_info: dict = {
    key: value
    for key, value in character_data.items()
    if key in basic_fields
  }

  profile_fields: list[str] = [
    "hair_color",
    "skin_color",
    "eye_color",
    "gender",
  ]

  profile: dict = {
    key: value
    for key, value in character_data.items()
    if key in profile_fields
  }

  summary: dict = {
    **basic_info,
    "character_id": character_id,
    "profile": profile,
    "source": "SWAPI",
  }

  return summary

def generate_crew(character_ids: list[int]) -> Generator[dict, None, None]:
  for character_id in character_ids:
    character = get_character(character_id)

    summary = create_character_summary(
      character,
      character_id,
    )

    yield summary

async def get_character_async(
    client: httpx.AsyncClient,
    character_id: int,
) -> Character:
    url: str = f"{BASE_URL}/people/{character_id}"

    response = await client.get(url)
    response.raise_for_status()
    data: dict = response.json()

    return Character(**data)

async def get_crew_async(
    client: httpx.AsyncClient,
    character_ids: list[int],
) -> list[Character]:

   
      tasks = [
        get_character_async(client, character_id)
        for character_id in character_ids
      ]

      characters = await asyncio.gather(*tasks)

      return characters

async def create_async_crew(
      character_ids: list[int],
) -> list[dict]:
   characters = await get_crew_async(character_ids)

   crew: list[dict] = [
      create_character_summary(character, character_id)
      for character, character_id in zip(
         characters,
         character_ids,
      )
   ]

   return crew

async def get_planet_async(
      client: httpx.AsyncClient,
      planet_id: int,
) -> dict:
   url: str = f"{BASE_URL}/planets/{planet_id}"

   response = await client.get(url)
   response.raise_for_status()

   return response.json()