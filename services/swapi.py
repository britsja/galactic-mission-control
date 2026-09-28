import requests
from models.character import Character

BASE_URL: str = "https://swapi.info/api"

def get_character(character_id: int) -> Character:
  url: str = f"{BASE_URL}/people/{character_id}"

  response = requests.get(url, timeout=5)

  response.raise_for_status()

  data: dict = response.json()

  character = Character(**data)

  return character