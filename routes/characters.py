from flask import Blueprint, jsonify

characters_bp = Blueprint("characters", __name__)

@characters_bp.route("/<int:character_id>", methods=["GET"])
def get_character(character_id: int):
  characters: dict[int, dict[str, str | int]] = {
    1: {
        "name": "Luke Skywalker",
        "height": 172,
        "birth_year": "19BBY",
        "homeworld": "Tatooine",
    },
    2: {
        "name": "C-3PO",
        "height": 167,
        "birth_year": "112BBY",
        "homeworld": "Tatooine",
    },
    3: {
        "name": "R2-D2",
        "height": 96,
        "birth_year": "33BBY",
        "homeworld": "Naboo",
    },
  }

  character = characters.get(character_id)

  if character is None:
    return jsonify({"error": "Character not found"}), 404

  return jsonify(character), 200