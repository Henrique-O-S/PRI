import scrapy.crawler as crawler
from src.Database import Database
from src.scraper.spiders.bigarticles import BigArticlesSpider
import json
from src.analyzer import Analyzer
from datetime import datetime

if __name__ == "__main__":

    with open('data/articles.json', 'r') as json_file:
        try:
            articles_data = json.load(json_file)
        except:
            articles_data = None

    database = Database()

    if articles_data is None:
        spider_big_articles_class = BigArticlesSpider
        spider_big_articles_class.database = database

        settings = {
                'FEEDS': {
                    'data/articles.json': {
                        'format': 'json',
                        'encoding': 'utf8',
                        'store_empty': False,
                        'fields': None,
                    },
                }
            }
        
        print("There is no articles data, scraping it now...")

        database.clearDatabase()

        process = crawler.CrawlerProcess(settings=settings)
        process.crawl(spider_big_articles_class)
        process.start()

        with open('data/articles.json', 'r') as json_file:
            try:
                articles_data = json.load(json_file)
            except:
                articles_data = None
        if articles_data is None:
            print("Failed to retrieve articles data")
            exit(1)

    print("Adding articles to database...")

    analyzer = Analyzer()

    for article in articles_data:
        keywords = analyzer.extract_keywords(article['text'])

        date = datetime.strptime(article['date'], "%Y-%m-%d %H:%M:%S")

        database.addArticletoDB(article['link'], article['title'], date, article['text'], article['keypoints'], article['author'], keywords)
        print(f"Added {article['title']} to database successfuly")
