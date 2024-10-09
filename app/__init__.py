from flask import Flask

def create_app():
    app = Flask(__name__)

    # Load configuration from .env file if needed
    app.config.from_pyfile('.env', silent=True)  # Ensure it doesn't raise an error if the .env file is missing

    # Import routes after creating the app to avoid circular imports
    from app.app import register_routes
    register_routes(app)  # Register routes with the app instance

    return app
