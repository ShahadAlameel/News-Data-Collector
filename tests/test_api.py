import unittest
from flask import Flask
from app import search_articles

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.add_url_rule('/news_articles', 'search_articles', search_articles, methods=['GET'])
        self.client = self.app.test_client()

    def test_search_articles_with_keyword(self):
        response = self.client.get('/news_articles?keyword=heart')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_search_articles_without_keyword(self):
        response = self.client.get('/news_articles')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
