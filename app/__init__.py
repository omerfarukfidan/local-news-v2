import os
import json
from flask import Flask
from flask_cors import CORS

def load_config():
    environment = os.getenv("ENVIRONMENT", "local")

    if environment == "local":
        # env for local
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, 'config.json')
        with open(config_path) as config_file:
            config = json.load(config_file)
        return config
    else:
        # env for lambda 
        config = {
            "DB_SERVER": os.getenv("DB_SERVER"),
            "DB_PORT": os.getenv("DB_PORT"),
            "DB_NAME": os.getenv("DB_NAME"),
            "DB_USER": os.getenv("DB_USER"),
            "DB_PASSWORD": os.getenv("DB_PASSWORD"),
            "DB_SSL_MODE": os.getenv("DB_SSL_MODE"),
            "ALLOWED_ORIGIN": os.getenv("ALLOWED_ORIGIN")
        }
        return config

def create_app():
    app = Flask(__name__)

    # Load configuration
    config = load_config()
    allowed_origin = config["ALLOWED_ORIGIN"]

    # Configure CORS
    CORS(app, resources={r"/*": {"origins": [allowed_origin]}})

    from app.routes import main_routes
    app.register_blueprint(main_routes)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
