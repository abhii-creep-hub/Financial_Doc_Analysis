import os
from flask import Flask
from app.routes import main

app = Flask(
    __name__,
    template_folder="app/templates",
    static_folder="app/static"
)

app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")


app.config["ENV"] = os.environ.get("FLASK_ENV", "development")
app.config["DEBUG"] = True


UPLOAD_FOLDER = os.path.join("app", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


app.register_blueprint(main)

@app.errorhandler(Exception)
def handle_error(e):
    print("FULL ERROR:", e)
    return f"<h2>ERROR:</h2><pre>{str(e)}</pre>", 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)