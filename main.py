from src.Database import Database
from src.scraper.spiders.articles import ArticlesSpider
from src.scraper.spiders.bigarticles import BigArticlesSpider

import scrapy.crawler as crawler


if __name__ == "__main__":
    database = Database()
    spider_class = ArticlesSpider
    spider_big_class = BigArticlesSpider
    spider_big_class.database = database
    spider_class.database = database

    settings = {
        'FEEDS': {
            'articles.json': {
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

    process = crawler.CrawlerProcess(settings)

    spider_class.links_to_save = spider_big_class.new_items

    process.crawl(spider_class)
    process.start()

