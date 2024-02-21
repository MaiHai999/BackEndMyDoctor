from flask import Flask
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy

class MyCustomApp:
    def __init__(self):
        self._app = Flask(__name__)
        CORS(self._app)
        self._app.config['CORS_HEADERS'] = 'Content-Type'

    def connect_database(self , user_name , password  , database = 'MyDoctor'):
        database_uri = 'mysql+mysqlconnector://{user_name}:{password}@localhost/{database}'
        database_uri = database_uri.format(user_name=user_name, password=password, database=database)

        self._app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
        self._app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    def get_model(self):
        db = SQLAlchemy(self._app)
        return db

    def get_app(self):
        return self._app





