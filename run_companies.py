import scrapy.crawler as crawler
from src.scraper.spiders.companies import CompaniesSpider

spider_class = CompaniesSpider
process = crawler.CrawlerProcess()
process.crawl(spider_class)
process.start()