import requests
from models.character import Character
from utils.decorators import log_execution_time
from collections.abc import Generator

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