import scrapy
from pymongo import MongoClient
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class GuardianSpider(scrapy.Spider):
    name = "guardian"
    start_urls = ["https://www.theguardian.com/au"]

    def parse(self, response):
        articles = response.xpath('//a[contains(@data-link-name, "news")]')
        for article in articles:
            article_url = article.xpath('@href').get()
            yield response.follow(article_url, self.parse_article)

    def parse_article(self, response):
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
        client = MongoClient(self.crawler.settings.get('MONGODB_URI'))
        db = client[self.crawler.settings.get('MONGODB_DATABASE')]
        collection = db[self.crawler.settings.get('MONGODB_COLLECTION')]
        collection.insert_one(data)

if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl(GuardianSpider)
    process.start()