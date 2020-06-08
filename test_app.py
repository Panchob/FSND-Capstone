import os
import unittest
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import *


ADMIN_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkFkMFVJY2NsTU1HWnF5a2hRSm5zcSJ9.eyJpc3MiOiJodHRwczovL3BhbmNob2IuYXV0aDAuY29tLyIsInN1YiI6ImVSNUdJOGxsYmZMQUhaMHVhVmxJS2RjZWZITE1qUjA2QGNsaWVudHMiLCJhdWQiOiJsZV9taXRyb24iLCJpYXQiOjE1OTE2MjYwOTAsImV4cCI6MTU5MTcxMjQ5MCwiYXpwIjoiZVI1R0k4bGxiZkxBSFowdWFWbElLZGNlZkhMTWpSMDYiLCJzY29wZSI6InBvc3Q6cmVjaXBlcyBwYXRjaDpyZWNpcGVzIHBvc3Q6Y2F0ZWdvcmllcyBkZWxldGU6cmVjaXBlcyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbInBvc3Q6cmVjaXBlcyIsInBhdGNoOnJlY2lwZXMiLCJwb3N0OmNhdGVnb3JpZXMiLCJkZWxldGU6cmVjaXBlcyJdfQ.EgioqpPWxO9nUk2sxFGeJbFPNOauWT77K5mAoGxCrsJpIRRgTyIvbn65O6mh9Cd1IssBH4c9nnBBdRETieCY_aIMbexDU5vD6EmA3YRacH2A4SOoaiz19IEJJEvcalTKs_pYllN1X7DstB0ggNcFGydAhIrR2YgiFVWdDjHGjfvuqUbleFjDrJF6IxLqnp1cIUXHayIXMRwlScsQwQDXfJPS2DxDxTWFcpNXrQtrlotFyY2XTeX6nW3rgDX_t7BLKo4OHtA3nxzv4wfHU3yEX9JHPHoDPSJvsg519MBVqhhC8yrLsxuigRNnGamn_gvOnXY9xzltrSm1S20NtrQ4UA'
EDITOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkFkMFVJY2NsTU1HWnF5a2hRSm5zcSJ9.eyJpc3MiOiJodHRwczovL3BhbmNob2IuYXV0aDAuY29tLyIsInN1YiI6ImVSNUdJOGxsYmZMQUhaMHVhVmxJS2RjZWZITE1qUjA2QGNsaWVudHMiLCJhdWQiOiJsZV9taXRyb24iLCJpYXQiOjE1OTE2MjYyMTMsImV4cCI6MTU5MTcxMjYxMywiYXpwIjoiZVI1R0k4bGxiZkxBSFowdWFWbElLZGNlZkhMTWpSMDYiLCJzY29wZSI6InBvc3Q6cmVjaXBlcyBwYXRjaDpyZWNpcGVzIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOlsicG9zdDpyZWNpcGVzIiwicGF0Y2g6cmVjaXBlcyJdfQ.Dw7frMHaGpQLw5bZhp829xz1OOQ0tgXz7J8049Gx7yfNlcwanMlR6471lG01iF8auv3BxYkMHh6nyzSEjoHbzcXOc-Y207VxLe7QelceLIz8bgbVklDMeLWPSIfa6oBinLZp2oVYwVj2j5S2BwbRy2nQ10xqXzkBmAXWCn5DF4NPC2HzUs-DYjr744Mgs1MgIvQUo4YPA1-jQqbe8VEHZmTqkc_nWyGqJ2cIhlCnB8s3J_zMb_HJ5yiIir8EHpJk8smjmvqENSWYRFtHS5noE20o2Sl_ESlqxHGZeD0pOarS_kDcZTCLrAUiTisMoSaeyP-E4KjsUsXDsrKKVAgL7w'


class MitronTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

        self.database_path = "postgres://postgres:61785@localhost:5432/mitron_test"
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            db_drop_and_create_all()

        categories = [Category("Bread"),
                      Category("Cake")]
        recipes = [Recipe("Sandwich bread",
                          "3h",
                          "Symmetrical butter receptacle",
                          "many",
                          2),
                   Recipe("Cake",
                          "1h",
                          "Symmetrical butter receptacle",
                          "many",
                          1)]

        ingredients = [Ingredient("flour"),
                       Ingredient("water"),
                       Ingredient("salt")]
        measurements = [Measurement("cups"),
                        Measurement("tsp")]

        quantities = [Quantity("3", 1, 1, 1),
                      Quantity("1", 2, 1, 1),
                      Quantity("1 1/2", 3, 2, 1)]

        try:
            for recipe in recipes:
                db.session.add(recipe)
            for category in categories:
                db.session.add(category)
            for ingredient in ingredients:
                db.session.add(ingredient)
            for measurement in measurements:
                db.session.add(measurement)
            db.session.commit()
            for quantity in quantities:
                db.session.add(quantity)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

        self.new_recipe = {
            'name': "Banana bread",
            'time': "1h",
            'description': "Unworthy fruits second chance",
            'instructions': "no",
            'category': 2
        }

        self.new_category = {
            'name': "Sourdough"
        }

    def tearDown(self):
        pass

    def test_get_index(self):
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)

    def test_get_recipes(self):
        res = self.client().get('/recipes?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_get_recipes(self):
        res = self.client().get('/recipes?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_get_categories(self):
        res = self.client().get('/category')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_search_recipe(self):
        res = self.client().post('/recipes', json={'searchTerm': "Bread"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['recipes']))

    def test_create_recipe(self):
        res = self.client().post('/recipes/create',
                                 headers={
                                     "Authorization": "Bearer {}".format(
                                         EDITOR_TOKEN
                                         )}, json=self.new_recipe)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_delete_recipe(self):
        res = self.client().delete('/recipes/2',
                                   headers={
                                       "Authorization": "Bearer {}".format(
                                           ADMIN_TOKEN)})
        data = json.loads(res.data)

        recipe = Recipe.query.filter(Recipe.id == 2).one_or_none()
        db.session.commit()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)
        self.assertEqual(recipe, None)

    def test_delete_unknown_recipe(self):
        res = self.client().delete('/recipes/99999',
                                   headers={
                                       "Authorization": "Bearer {}".format(
                                           ADMIN_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_create_category(self):
        res = self.client().post('/categories/create',
                                 headers={
                                     "Authorization": "Bearer {}".format(
                                         ADMIN_TOKEN)
                                 }, json=self.new_category)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_unauthorize_create_category(self):
        res = self.client().post('/categories/create',
                                 headers={
                                     "Authorization": "Bearer {}".format(
                                         EDITOR_TOKEN)
                                 }, json=self.new_category)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)

    def test_list_recipes_from_category(self):
        res = self.client().get('/categories/1/recipes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['recipes']))

    def test_list_ingredients_from_category(self):
        res = self.client().get('/recipes/1/ingredients')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['ingredients']))

    def test_list_recipes_non_existing_category(self):
        res = self.client().get('/categories/9999/recipes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_modify_recipe(self):
        res = self.client().patch('/recipes/1/modify',
                                  headers={
                                      "Authorization": "Bearer {}".format(
                                          EDITOR_TOKEN)
                                      }, json={'time': "20m"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_modify_recipe(self):
        res = self.client().patch('/recipes/1/modify',
                                  headers={
                                      "Authorization": "Bearer {}".format(
                                          EDITOR_TOKEN)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

if __name__ == "__main__":
    unittest.main()
