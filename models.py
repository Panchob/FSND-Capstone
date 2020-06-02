import os
from sqlalchemy import Column, String, create_engine, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

database_path = os.environ.get('DATABASE_URL')
if not database_path:
    database_path = "postgres://postgres:61785@localhost:5432/mitron"

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    migrate = Migrate(app, db)
    db.init_app(app)



class Category(db.Model):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    recipes =  db.relationship('Recipe', backref='category', lazy=True)

class Recipe(db.Model):
    __tablename__ = 'recipe'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    time = Column(DateTime)
    description = Column(String(500))
    instruction = Column(String(5000))
    
class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True)
    name = Column(String)
