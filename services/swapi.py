import requests

BASE_URL: str = "https://swapi.info/api"

def get_character(character_id: int) -> dict:
  url: str = f"{BASE_URL}/people/{character_id}"

  response = requests.get(url, timeout=5)

  response.raise_for_status()

  return response.json()