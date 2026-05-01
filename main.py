import os
from flask import Flask
from flask_login import LoginManager
from app.routes import main
from app.models import db, User

app = Flask(
    __name__,
    template_folder="app/templates",
    static_folder="app/static"
)

app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

# DATABASE
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# LOGIN
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "main.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# CREATE DB
with app.app_context():
    db.create_all()

# UPLOAD FOLDER
UPLOAD_FOLDER = os.path.join("app", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.register_blueprint(main)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)