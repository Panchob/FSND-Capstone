import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

database_path = os.environ.get('DATABASE_URL')
if not database_path:
    database_name = "mitron"
    database_pat = "postgres://{}@{}/{}".format('postgres: 61785',
                                                'localhost: 5432',
                                                 database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    #db.create_all()

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    recipes =  db.relationship('Recipe', backref='category', lazy=True)

class Recipe(db.Model):
    __tablename__ = 'recipe'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.relationship('Ingredient', backref='recipe', lazy=True)
    time = db.Column(db.DateTime)
    description = db.Column(db.String(500))
    instruction = db.Column(db.String(5000))
    
class Ingredient(db.Model):
    __tablename__ = 'ingredient'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String)


