import os
import json
import subprocess
from unittest import TestCase, main, mock
from flask_sqlalchemy import SQLAlchemy

from api import create_app
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
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_url = get_database_url(db_name)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def test_check_health(self):
        response = self.client.get('/health')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])


if __name__ == '__main__':
    main()
