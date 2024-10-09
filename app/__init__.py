from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Load configuration from .env file or other sources if needed
    app.config.from_pyfile('.env')
    
    return app
