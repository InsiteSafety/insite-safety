# Standard library imports

# Remote library imports
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

def configure_server():
    """Creates and returns new instance of Flask with the appropriate attributes.
    The attributes depend on the configuration type.

    Raises:
        ValueError: if the configuration type read from configType.txt is neither DEVELOPMENT nor SERVER.

    Returns:
        Flask: the appropriate instation of Flask for this application.
    """
    with open("../configType.txt", encoding="utf-8") as mode:
        config_type = mode.read()
    if config_type.lower() == 'development':
        return Flask(__name__)
    elif config_type.lower() == 'production':
        return Flask(
            __name__,
            static_url_path="",
            static_folder="../client/dist",
            template_folder="../client/dist",
        )
    else:
        raise ValueError("Invalid configuration type processed.")
    
app = configure_server()
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

db = SQLAlchemy()
migrate = Migrate(app, db)
db.init_app(app)

# Instantiate REST API
api = Api(app)

# Instantiate CORS
CORS(app)

bcrypt = Bcrypt(app)