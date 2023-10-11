import scrapy.crawler as crawler
from src.scraper.spiders.companies import CompaniesSpider
from src.Database import Database
import json
from src.analyzer import Analyzer


if __name__ == "__main__":

    with open('data/companies.json', 'r') as json_file:
        try:
            companies_data = json.load(json_file)
        except:
            companies_data = None

    database = Database()

    if companies_data is None:
        spider_class = CompaniesSpider
        spider_class.database = database

        settings = {
            'FEEDS': {
                'data/companies.json': {
                    'format': 'json',
                    'encoding': 'utf8',
                    'store_empty': False,
                    'fields': None,
                },
            }
        }

        print("There is no companies data, scraping it now...")

        process = crawler.CrawlerProcess(settings)
        process.crawl(spider_class)
        process.start()

        with open('data/companies.json', 'r') as json_file:
            try:
                companies_data = json.load(json_file)
            except:
                companies_data = None
        if companies_data is None:
            print("Failed to retrieve companies data")
            exit(1)
        print("Companies data retrieved successfully")

    print("Adding companies to database...")

    analyzer = Analyzer()
    for company in companies_data:
        keywords = analyzer.extract_keywords(company['description'])
        tag = company['link'].split('/')[-1]
        database.addCompanytoDB(company['link'], tag, company['name'], company['description'], keywords)
        print(f"Added {company['name']} to database successfuly")


