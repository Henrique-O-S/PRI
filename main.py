from src.scraper.spiders.articles import ArticlesSpider
import scrapy.crawler as crawler

if __name__ == "__main__":
    spider_class = ArticlesSpider

    process = crawler.CrawlerProcess()
    process.crawl(spider_class)
    process.start()