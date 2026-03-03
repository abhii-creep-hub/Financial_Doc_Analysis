"""
Application Entry Point
Run this file to start the Flask development server
"""

import os
from app import create_app, db
from flask_migrate import upgrade

# Get environment from system or default to development
env = os.environ.get('FLASK_ENV', 'development')

# Create Flask app
app = create_app(env)

# Context for Flask shell
@app.shell_context_processor
def make_shell_context():
    """Make db available in Flask shell"""
    return {'db': db}


if __name__ == '__main__':
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()
        print("Database tables created/verified")

    # Start development server
    # Note: In production, use gunicorn instead
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=(env == 'development'),
        use_reloader=True
    )
