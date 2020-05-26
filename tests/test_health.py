import os
import json
import subprocess
from unittest import TestCase, main, mock
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from util import get_database_url

db_name = 'casting_test'

class HealthTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run(
            ['dropdb', db_name, '--if-exists'],
            stdout=subprocess.DEVNULL
        )
        subprocess.run(
            ['createdb', db_name],
            stdout=subprocess.DEVNULL
        )

    def setUp(self):
        database_url = get_database_url(db_name)
        self.app = create_app(database_url)
        self.client = self.app.test_client()

        with self.app.app_context():
            self.db = SQLAlchemy(self.app)
            self.db.create_all()

    def test_check_health(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = json.loads(response.data)
        self.assertIn('success', data)
        self.assertTrue(data['success'])


if __name__ == '__main__':
    main()
