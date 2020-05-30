import json
from unittest import TestCase, main

from app import create_app
from models.database import db
from util import get_database_url


class HealthTestCase(TestCase):
    def setUp(self):
        self.db_name = 'casting_test'
        self.app = create_app(get_database_url(self.db_name))
        self.client = self.app.test_client()

        with self.app.app_context():
            self.db = db
            self.db.drop_all()
            self.db.create_all()

    def tearDown(self):
        with self.app.app_context():
            self.db.drop_all()

    def test_check_health(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        data = json.loads(response.data)
        self.assertIn('success', data)
        self.assertTrue(data['success'])


if __name__ == '__main__':
    main()
