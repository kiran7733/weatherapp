import unittest
from app import app

class WeatherAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page_loads(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'City', response.data)

    def test_invalid_city(self):
        response = self.app.post('/', data=dict(city="InvalidCityName"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'City not found', response.data)

if __name__ == '__main__':
    unittest.main()
