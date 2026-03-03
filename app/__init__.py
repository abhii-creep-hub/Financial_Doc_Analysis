"""
Flask Application Factory
Initializes and configures the Flask app with all extensions
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

# Configure logging
logger = logging.getLogger(__name__)


def create_app(config_name='development'):
    """
    Application factory function that creates and configures the Flask app.

    Args:
        config_name (str): Configuration environment name

    Returns:
        Flask: Configured Flask application instance
    """
    from config import config

    # Create Flask app instance
    app = Flask(__name__)

    # Load configuration based on environment
    app.config.from_object(config[config_name])

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)

    # Create upload folder if doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('logs', exist_ok=True)

    # Setup logging
    _setup_logging(app)

    # Register database commands
    _register_db_commands(app)

    # Register blueprints (routes)
    _register_blueprints(app)

    # Register error handlers
    _register_error_handlers(app)

    logger.info(f"Flask app created with config: {config_name}")
    return app


def _setup_logging(app):
    """Configure application logging"""
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)

    # File handler for app logs
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'app.log'),
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Financial Document Analysis System started')


def _register_db_commands(app):
    """Register custom database commands"""

    @app.shell_context_processor
    def make_shell_context():
        """Add db to shell context for easier access"""
        return {'db': db}


def _register_blueprints(app):
    """Register all route blueprints"""
    # We'll add blueprints here as we create them
    # Example structure:
    # from app.routes.document import document_bp
    # app.register_blueprint(document_bp)
    pass


def _register_error_handlers(app):
    """Register error handlers for common HTTP errors"""

    @app.errorhandler(404)
    def page_not_found(error):
        return {'error': 'Page not found'}, 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500

    @app.errorhandler(413)
    def request_entity_too_large(error):
        return {'error': 'File size too large. Max 50MB allowed'}, 413
