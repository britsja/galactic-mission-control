from flask import Flask

app = Flask(__name__)

@app.route("/")
def home() -> str:
  return """
    <h1>Galactic Mission Control</h1>
    <p>System Status: Online</p>
  """

if __name__ == "__main__":
  app.run(debug=True)