import os
from flask import Flask
from app.routes import main

app = Flask(
    __name__,
    template_folder="app/templates",
    static_folder="app/static"
)

# Secret key
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

# Production config
app.config["ENV"] = os.environ.get("FLASK_ENV", "production")
app.config["DEBUG"] = False

# Ensure upload folder exists
UPLOAD_FOLDER = os.path.join("app", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Register routes
app.register_blueprint(main)

# Run only locally (Render uses gunicorn)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)