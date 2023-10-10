import scrapy.crawler as crawler
from src.Database import Database
from src.scraper.spiders.articles import ArticlesSpider
from src.scraper.spiders.bigarticles import BigArticlesSpider

database = Database()
spider_class = ArticlesSpider
spider_big_class = BigArticlesSpider

spider_big_class.database = database
spider_class.database = database

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
process = crawler.CrawlerProcess(settings)
process.crawl(spider_big_class)
process.start()