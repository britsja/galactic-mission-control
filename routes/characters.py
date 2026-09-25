from flask import Blueprint, jsonify
import requests
from services.swapi import get_character

characters_bp = Blueprint("characters", __name__)

@characters_bp.route("/<int:character_id>", methods=["GET"])
def character_by_id(character_id: int):
  try:
    character = get_character(character_id)
  except requests.exceptions.HTTPError as error:
    if error.response.status_code == 404:
      return jsonify({"error": "Character not found"}), 404

    return jsonify({"error": "SWAPI request failed"}), 502
  except requests.exceptions.RequestException:
    return jsonify({"error": "Unable to connect to SWAPI"}), 503

  return jsonify(character), 200