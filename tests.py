import datetime
import os
import time
import unittest
 
from sandwalker import create_app
from sandwalker import models, routes


class BasicTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        with self.app.app_context():
            models.db.create_all()
            self.test_app = self.app.test_client()
            models.db.session.add(
                models.TimelineEntry(account='84', block=25000, amount=1000000, time=datetime.date.fromisoformat('2021-05-21')))
            models.db.session.commit()
 
    def tearDown(self):
        with self.app.app_context():
            models.db.session.close()
            models.db.drop_all()

    def test_home(self):
        response = self.test_app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        assert 'Current Height is <b>25000</b>' in str(response.data)

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

    def test_explore_rewards_found(self):
        response = self.test_app.get('/explore/84', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        assert '1 rewards earned' in str(response.data)
        assert '1.000 <small class="exp">pokt</small> minted' in str(response.data)

    def test_api_rewards_all(self):
        response = self.test_app.get('/api/rewards/84', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, response.json['count'])
        self.assertEqual(None, response.json['error'])
        self.assertEqual(1000000, response.json['total'])
        self.assertEqual({
            '2021-05-01': {
                'entries': [{
                    'amount': 1000000,
                    'block': 25000,
                    'current_count': 1,
                    'current_month_total': 1000000,
                    'current_total': 1000000
                }],
                'month_total': 1000000}}, response.json['all_entries'])


if __name__ == "__main__":
    unittest.main()
