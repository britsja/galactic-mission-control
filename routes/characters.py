from flask import Blueprint, jsonify
import requests
from pydantic import ValidationError
from services.swapi import get_character, create_character_summary, generate_crew


characters_bp = Blueprint("characters", __name__)

@characters_bp.route("/crew", methods=["GET"])
def get_crew():
  crew_ids: list[int] = [1, 5, 10, 13]

  crew_generator = generate_crew(crew_ids)
  crew: list[dict] = list(crew_generator)

  return jsonify({
    "crew": crew,
    "crew_size": len(crew),
  }), 200

@characters_bp.route("/<int:character_id>", methods=["GET"])
def character_by_id(character_id: int):
  try:
    character = get_character(character_id)

    summary = create_character_summary(
      character,
      character_id,
    )
  except requests.exceptions.HTTPError as error:
    if error.response.status_code == 404:
      return jsonify({"error": "Character not found"}), 404

    return jsonify({"error": "SWAPI request failed"}), 502
  except requests.exceptions.RequestException:
    return jsonify({"error": "Unable to connect to SWAPI"}), 503

  except ValidationError:
    return jsonify({"error": "Invalid character data received from Swapi"}), 502

  return jsonify(summary), 200