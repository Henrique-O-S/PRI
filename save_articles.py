import scrapy.crawler as crawler
from src.Database import Database
from src.scraper.spiders.articles import ArticlesSpider
from src.scraper.spiders.bigarticles import BigArticlesSpider
import os

spider_class = ArticlesSpider
spider_big_class = BigArticlesSpider

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


def erase_json_file_contents(file_path):
    try:
        # Open the file in write mode to truncate and erase its contents
        with open(file_path, "w", encoding='utf-8') as f:
            f.write('{}')
        print("Contents of the JSON file erased.")
    except FileNotFoundError:
        print("FILE NOT FOUND")


current_directory = os.getcwd()
file_path = os.path.join(current_directory, "links_to_save.json")
#erase_json_file_contents(file_path)