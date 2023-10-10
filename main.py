import scrapy.crawler as crawler
from src.Database import Database
from src.scraper.spiders.articles import ArticlesSpider
from src.scraper.spiders.bigarticles import BigArticlesSpider
from scrapy import signals
from scrapy.signalmanager import dispatcher

database = Database()
spider_articles_class = ArticlesSpider
spider_big_articles_class = BigArticlesSpider

spider_big_articles_class.database = database
spider_articles_class.database = database

settings = {
    'FEEDS': {
        'links_to_save.json': {
            'format': 'json',
            'encoding': 'utf8',
            'store_empty': False,
            'fields': None,
        },
    }
}

class Runner:
    def __init__(self):
        self.process = crawler.CrawlerProcess(settings=settings)

        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.run_next_spider()

    def run_next_spider(self):
        if not hasattr(self, 'spider_big_articles_class_done'):
            self.process.crawl(spider_big_articles_class)
            self.spider_big_articles_class_done = True
        elif not hasattr(self, 'spider_articles_class_done'):
            self.process.crawl(spider_articles_class,)
            self.spider_articles_class_done = True
        else:
            self.process.stop()

    def spider_closed(self, spider, reason):
        self.run_next_spider()

if __name__ == "__main__":
    database.clearDatabase()

    runner = Runner()
    runner.process.start()

    database.write_saved_links()
    database.erase_links_to_save()

