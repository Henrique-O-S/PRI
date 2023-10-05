from src.scraper.spiders.articles import ArticlesSpider
from src.scraper.spiders.bigarticles import BigArticlesSpider

import scrapy.crawler as crawler

if __name__ == "__main__":
    spider_class = ArticlesSpider
    #spider_class = BigArticlesSpider call this for the calendar scrapping (NOT FINISHED YET

    process = crawler.CrawlerProcess()
    process.crawl(spider_class)
    process.start()