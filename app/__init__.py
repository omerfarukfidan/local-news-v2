import os
import json
from flask import Flask
from flask_cors import CORS

# Helper function to load config.json
def load_config():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, 'config.json')
    with open(config_path) as config_file:
        return json.load(config_file)

def create_app():
    app = Flask(__name__)

    # Load ALLOWED_ORIGIN from config.json
    config = load_config()
    allowed_origin = config["ALLOWED_ORIGIN"]

    # Configure CORS for the entire app
    CORS(app, resources={r"/*": {"origins": [allowed_origin]}})

    from app.routes import main_routes
    app.register_blueprint(main_routes)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
