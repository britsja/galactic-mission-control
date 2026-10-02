import asyncio
import httpx
from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from models.mission import MissionRequest
from services.missions import build_mission

missions_bp = Blueprint("missions", __name__)

@missions_bp.route("", methods=["POST"])
def create_mission():
  data = request.get_json(silent=True)
  if data is None:
    return jsonify({
      "error": "Request body must contain valid JSON"
    }), 400

  try:
    mission_request = MissionRequest(**data)

    mission = asyncio.run(
      build_mission(mission_request)
    )
  except ValidationError as error:
    return jsonify({
      "error": "Invalid mission data",
      "details": error.errors(),
    }), 400

  except httpx.HTTPStatusError as error:
    if error.response.status_code == 404:
      return jsonify({
        "error": "Character of planet not found"
      }), 404

    return jsonify({
      "error": "SWAPI request failed"
    }), 502

  except httpx.RequestError:
    return jsonify({
      "error": "Unable to connect to Swapi"
    }), 503

  return jsonify(mission), 201