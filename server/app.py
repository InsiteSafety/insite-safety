# app.py
from flask import request, session
from flask_restful import Resource

from config import app, db, api # This line will run the config.py file and initialize our app
from models.user import User
from models.models import * 

# All routes here!

if __name__ == '__main__':
    app.run(port=4000, debug=True)