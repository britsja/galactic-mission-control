import asyncio
import httpx
from models.mission import MissionRequest
from services.swapi import (
  get_crew_async,
  get_planet_async,
  create_character_summary
)

async def build_mission(
    mission: MissionRequest,
) -> dict:
  async with httpx.AsyncClient(timeout=5.0) as client:
    crew_task = get_crew_async(
      client,
      mission.character_ids,
    )

    planet_task = get_planet_async(
      client,
      mission.planet_id,
    )

    characters, planet = await asyncio.gather(
      crew_task,
      planet_task,
    )

  crew: list[dict] = [
    create_character_summary(character, character_id)
    for character, character_id in zip(
      characters,
      mission.character_ids,
    )
  ]

  return {
    "mission_name": mission.mission_name,
    "destination": planet["name"],
    "crew": crew,
    "crew_size": len(crew),
    "status": "MISSION READY",
  }