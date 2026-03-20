import unittest
from api.app import app

class TestRecAPI(unittest.TestCase):
    def setUp(self):
        # setup flask test client
        app.testing = True
        self.client = app.test_client()
        
    def test_health(self):
        res = self.client.get('/health')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['status'], 'ok')
        
    def test_recommend_known_user(self):
        res = self.client.get('/recommend/u1')
        self.assertEqual(res.status_code, 200)
        self.assertIn('recommendations', res.json)
        self.assertTrue(len(res.json['recommendations']) > 0)
        
    def test_recommend_unknown_user(self):
        res = self.client.get('/recommend/ghost_user')
        self.assertEqual(res.status_code, 404)
        
    def test_missing_feedback_data(self):
        res = self.client.post('/feedback', json={"uid": "u1"}) # missing cid/rating
        self.assertEqual(res.status_code, 400)

if __name__ == '__main__':
    unittest.main()