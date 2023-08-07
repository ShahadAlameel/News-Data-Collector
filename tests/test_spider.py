import unittest
from unittest.mock import patch, MagicMock
from scrapy.http import TextResponse
from scrapy.utils.test import get_crawler
from guardian_articles.guardian_articles.spiders.guardian_spider import GuardianSpider

class TestGuardianSpider(unittest.TestCase):
    '''
    Test class for GuardianSpider.

    This class contains test methods to verify the functionality of the GuardianSpider
    spider, including parsing article data and saving to MongoDB.
    '''

    def setUp(self):
        '''
        Method to set up the test environment before each test case.
        '''

        # Create a dummy crawler object
        self.dummy_crawler = get_crawler(spidercls=GuardianSpider)

    @patch('guardian_articles.guardian_articles.spiders.guardian_spider.MongoClient')
    def test_parse_article_data_extraction(self, mock_mongo_client):
        '''
        Test method to verify the parsing of an article page.

        This test uses a mocked response object to simulate an article page and checks
        whether the parsing logic correctly extracts the article title, content, and
        author information.
        '''

        # Sample test data for the response
        sample_article_url = "https://www.theguardian.com/au/some-article"
        sample_article_title = "Sample Article Title"
        sample_article_text = "This is a sample article content."
        sample_article_author = "John Doe"

        # Create the spider instance
        spider = GuardianSpider(self.dummy_crawler)

        # Create a sample response 
        response = TextResponse(url=sample_article_url, body=f"<h1>{sample_article_title}</h1><div class='article-body-viewer-selector'><p>{sample_article_text}</p></div><address aria-label='Contributor info'><div><a>{sample_article_author}</a></div></address>", encoding='utf-8')

        # Test the parse_article method
        article_data = next(spider.parse_article(response))

        # Verify that the data is correctly extracted
        expected_data = {
            "url": sample_article_url,
            "title": sample_article_title,
            "text": sample_article_text,
            "author": sample_article_author
        }
        self.assertEqual(article_data, expected_data)


if __name__ == "__main__":
    unittest.main()
