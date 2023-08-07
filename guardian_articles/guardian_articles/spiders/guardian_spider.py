import scrapy
from pymongo import MongoClient
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class GuardianSpider(scrapy.Spider):
    '''
    GuardianSpider is a Scrapy spider that crawls The Guardian's Australian edition
    (https://www.theguardian.com/au) and extracts news article data, including article
    title, content, and author information. The extracted data is then saved to a MongoDB
    database.
    '''

    name = "guardian"
    start_urls = ["https://www.theguardian.com/au"]

    def __init__(self, crawler):
        super(GuardianSpider, self).__init__()
        self.crawler = crawler

    def parse(self, response):
        '''
        Method for parsing the initial response and extracting article URLs.
        Args:
            response: The initial response from the start URL.
        Yields:
            scrapy.Request: A Request object for each article URL to be further parsed.
        '''

        articles = response.xpath('//a[contains(@data-link-name, "news")]')
        for article in articles:
            article_url = article.xpath('@href').get()
            yield response.follow(article_url, self.parse_article)

    def parse_article(self, response):
        '''
        Method for parsing an article page and extracting article information.
        Args:
            response: The response from the article URL.
        Yields:
            article_data: A dictionary containing the article information.
        '''

        article_title = response.xpath('//h1/text()').get()
        article_text = response.xpath('//div[contains(@class, "article-body-viewer-selector")]//p//text()').getall()
        article_text = " ".join(article_text).strip()
        article_author = response.xpath('//address[contains(@aria-label, "Contributor info")]//div//a//text()').getall()
        article_author = ", ".join(article_author).strip()

        article_data = {
            "url": response.url,
            "title": article_title,
            "text": article_text,
            "author": article_author,
        }


        # Save news articles data to MongoDB
        self.save_to_mongodb(article_data)

        yield article_data
    
    def save_to_mongodb(self, data):
        '''
        Method for saving news article data to MongoDB.
        Args:
            data: A dictionary containing the article information to be saved.
        '''

        client = MongoClient(self.crawler.settings.get('MONGODB_URI'))
        db = client[self.crawler.settings.get('MONGODB_DATABASE')]
        collection = db[self.crawler.settings.get('MONGODB_COLLECTION')]
        collection.insert_one(data)

if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl(GuardianSpider)
    process.start()