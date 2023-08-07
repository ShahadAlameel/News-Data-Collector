import unittest
from flask import Flask
from app import search_articles

class TestAPI(unittest.TestCase):
    '''
    Test class for testing the API endpoints.

    This class contains test methods to verify the behavior of the search_articles
    function, which is responsible for handling the /news_articles endpoint in the
    Flask application.
    '''

    def setUp(self):
        '''
        Set up the test environment before each test case.

        This method creates a Flask test client and adds the /news_articles endpoint
        with the search_articles function to the Flask application. The test client
        allows simulating HTTP requests to the application without running a server.
        '''

        self.app = Flask(__name__)
        self.app.add_url_rule('/news_articles', 'search_articles', search_articles, methods=['GET'])
        self.client = self.app.test_client()

    def test_search_articles_with_keyword(self):
        '''
        Test the /news_articles endpoint with a keyword.

        This method sends a GET request to the /news_articles endpoint with a keyword
        parameter. It verifies that the response status code is 200 (OK) and that the
        data returned by the endpoint is a list.
        '''

        response = self.client.get('/news_articles?keyword=heart')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_search_articles_without_keyword(self):
        '''
        Test the /news_articles endpoint without a keyword.

        This method sends a GET request to the /news_articles endpoint without a keyword
        parameter. It verifies that the response status code is 200 (OK) and that the
        data returned by the endpoint is a list.
        '''

        response = self.client.get('/news_articles')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
