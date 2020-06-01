import os
import unittest
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db

class MitronTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_pat = os.environ['DB_URL_TEST']
        
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

if __name__ == "__main__":
    unittest.main()