import scrapy.crawler as crawler
from src.Database import Database
from src.scraper.spiders.articles import ArticlesSpider
from src.scraper.spiders.bigarticles import BigArticlesSpider
import os

spider_class = ArticlesSpider
database = Database()
spider_class.database = database

settings = {
    'FEEDS': {
        'saved_links.json': {
            'format': 'json',
            'encoding': 'utf8',
            'store_empty': False,
            'fields': None,
        },
        'links_to_save.json': {
            'format': 'json',
            'encoding': 'utf8',
            'store_empty': False,
            'fields': None,
        },
    }
}

process = crawler.CrawlerProcess(settings)
process.crawl(spider_class)
process.start()

database.write_saved_links()
database.erase_links_to_save()
