import os
import unittest
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Recipe

class MitronTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "mitron_test"
        self.database_pat = "postgres://{}@{}/{}".format('postgres:61785',
                                                          'localhost:5432',
                                                          self.database_name)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        pass

    def test_get_index(self):
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)

    def test_get_recipes(self):
        res = self.client().get('/recipes')
        self.assertEqual(res.status_code, 200)
    
    def test_get_categories(self):
        res = self.client().get('/categories')
        data.loads(res.data)

        self.asserEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_search_recipe(self):
        res = self.client().post('/recipes', json={'searchTerm': "Title"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['recipes']))
    
    def test_create_recipe(self):
        res = self.client().post('/recipe/create')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_delete_recipe(self):
        res = self.client().delete('recipes/2')
        data = json.loads(res.data)

        recipe = Recipe.query.filter(Recipe.id == 10).one_ro_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 10)
        self.assertEqual(recipe, None)
    
    def test_delete_unknown_recipe(self):
        res = self.client.delete('recipe/99999')

        self.asserEqual(res.status_code, 422)
        self.asserEqual(data['success'], False)

    def test_list_recipes_from_category(self):
        res = self.client().get('/categories/1/recipes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['recipes']))

    def test_list_recipes_non_existing_category(self):
        res = self.client().get('/categories/9999/recipes')
        data = json.load(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_list_ingredients_from_recipe(self):
        res = self.client().get('/recipes/1/ingredients')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['ingredients']))

    def test_list_quantities_from_recipe(self):
        res = self.client().get('/recipes/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['quantities']))

    def test_modify_recipe(self):
        res = self.client().patch()
    

if __name__ == "__main__":
    unittest.main()