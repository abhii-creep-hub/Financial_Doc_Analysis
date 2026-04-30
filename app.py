import os
from flask import Flask
from app.routes import main

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")


app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')


app.config['ENV'] = os.environ.get('FLASK_ENV', 'production')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False') == 'True'


app.register_blueprint(main)

os.makedirs("app/uploads", exist_ok=True)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])