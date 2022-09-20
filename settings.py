from flask import Flask
from flasgger import Swagger
from flask_restful import Api

app = Flask(__name__)
swagger = Swagger(app)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TasksToDo.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
