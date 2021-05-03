import os
import unittest
 
from sandwalker import create_app
from sandwalker import models, routes


class BasicTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        with self.app.app_context():
            self.test_app = self.app.test_client()
 
    def tearDown(self):
        with self.app.app_context():
            models.db.session.close()
            models.db.drop_all()

    def test_home(self):
        response = self.test_app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_explorer(self):
        response = self.test_app.get('/explorer', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.test_app.get('/about', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_resources(self):
        response = self.test_app.get('/resources', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        assert 'Download Daily Dump' in str(response.data)

    def test_explore_nok(self):
        response = self.test_app.get('/explore', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_explore_not_found(self):
        response = self.test_app.get('/explore/42', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        assert 'No reward were found for 42' in str(response.data)
        
 
if __name__ == "__main__":
    unittest.main()
