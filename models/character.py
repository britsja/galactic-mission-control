from pydantic import BaseModel

class Character(BaseModel):
  name: str
  height: str
  mass: str
  hair_color: str
  skin_color: str
  eye_color: str
  birth_year: str
  gender: str
  homeworld: str

