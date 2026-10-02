from pydantic import BaseModel, Field

class MissionRequest(BaseModel):
  mission_name: str = Field(
    min_length=3,
    max_length=100,
  )

  character_ids: list[int] = Field(
    min_length=1,
    max_length=6,
  )

  planet_id: int = Field(gt=0)