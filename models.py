import os
from sqlalchemy import Column, String, create_engine, Integer
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


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

class Category(db.Model):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name
    
    def format(self):
        return {
            'name': self.name
        }

class Recipe(db.Model):
    __tablename__ = 'recipe'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    time = Column(String)
    description = Column(String(500))
    instructions = Column(String(5000))
    category = Column(Integer)
    ingredients = db.relationship("Quantity", backref='recipe', lazy=True, passive_deletes=True)

    def __init__(self, name, time, description, instructions, category):
        self.name = name
        self.time = time
        self.description = description
        self.instructions = instructions
        self.category = category

    def format(self):
        return{
            'id': self.id,
            'name': self.name,
            'time': self.time,
            'description': self.description,
            'instructions': self.instructions,
            'category': self.category
        }
    
class Ingredient(db.Model):
    __tablename__ = 'ingredient'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    quantity = db.relationship("Quantity", backref='ingredient', lazy=True, passive_deletes=True)

    def __init__(self, name):
        self.name = name

class Quantity(db.Model):
    __tablename__ = 'quantity'

    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, db.ForeignKey('recipe.id', ondelete="CASCADE"))
    ingredient_id = Column(Integer, db.ForeignKey('ingredient.id', ondelete="CASCADE"))
    measurement_id =  Column(Integer, db.ForeignKey('measurement.id', ondelete="CASCADE"))
    # String so it's possible to enter something like "3/4"
    quantity = Column(String)

    def __init__(self, quantity, ingredient_id, measurement_id, recipe_id):
        self.quantity = quantity
        self.ingredient_id = ingredient_id
        self.measurement_id = measurement_id
        self.recipe_id = recipe_id


class Measurement(db.Model):
    __tablename__ = 'measurement'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    quantity = db.relationship("Quantity", backref='measurement', lazy=True, passive_deletes=True)

    def __init__(self, name):
        self.name = name

