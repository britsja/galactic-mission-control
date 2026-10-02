from flask import Flask
from routes.characters import characters_bp
from routes.missions import missions_bp

app = Flask(__name__)

app.register_blueprint(
  characters_bp, url_prefix="/api/v1/characters"
)

app.register_blueprint(
  missions_bp, url_prefix="/api/v1/missions"
)

@app.route("/")
def home() -> str:
  return """
    <h1>Galactic Mission Control</h1>
    <p>System Status: Online</p>
  """

if __name__ == "__main__":
  app.run(debug=True)