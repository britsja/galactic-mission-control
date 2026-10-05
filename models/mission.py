from typing import Annotated
from pydantic import BaseModel, Field, field_validator

PositiveId = Annotated[int, Field(gt=0)]

class MissionRequest(BaseModel):
  mission_name: str = Field(
    min_length=3,
    max_length=100,
  )

  character_ids: list[PositiveId] = Field(
    min_length=1,
    max_length=6,
  )

  planet_id: PositiveId

  @field_validator("character_ids")
  @classmethod
  def character_ids_must_be_unique(
    cls,
    character_ids: list[int],
  ) -> list[int]:
    if len(character_ids) != len(set(character_ids)):
      raise ValueError(
        "Character IDs must be unique"
      )
    return character_ids