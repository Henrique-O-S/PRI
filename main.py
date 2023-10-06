from src.scraper.spiders.articles import ArticlesSpider
from src.scraper.spiders.bigarticles import BigArticlesSpider

import scrapy.crawler as crawler

if __name__ == "__main__":
    spider_class = ArticlesSpider
    spider_big_class = BigArticlesSpider

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
    process.crawl(spider_class)
    process.start()


