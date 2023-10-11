import argparse
import scrapy.crawler as crawler
from Database import Database
from scraper.spiders.bigarticles import BigArticlesSpider
from scraper.spiders.companies import CompaniesSpider
import json
from analyzer import Analyzer
from datetime import datetime

DEFAULT_START_YEAR = 2023
DEFAULT_CLEAR_DATABASE = False
DEFAULT_READ_STORED_DATA = False

database = Database()
analyzer = Analyzer()

companies_json_file_path = './data/companies.json'
articles_json_file_path = './data/articles.json'

companies_settings = {
    'FEEDS': {
        companies_json_file_path: {
            'format': 'json',
            'encoding': 'utf8',
            'store_empty': False,
            'fields': None,
        },
    }
}

articles_settings = {
    'FEEDS': {
        articles_json_file_path: {
            'format': 'json',
            'encoding': 'utf8',
            'store_empty': False,
            'fields': None,
        },
    }
}

def parse_arguments():
    parser = argparse.ArgumentParser(description=
            """Scrape articles from CNBC and store them in a database.""")
    parser.add_argument("-start", "--start_year", type=int, help="The starting year. Default is 2023.")
    parser.add_argument("-clear_db", "--clear_database", type=str, help="Clear the database? Y/N Default is N")
    parser.add_argument("-read_stored", "--read_stored_data", type=str, help="Read stored JSON data first? Y/N Default is N")
    
    args = parser.parse_args()
    
    start_year_arg = args.start_year
    clear_database_arg = args.clear_database
    read_stored_data_arg = args.read_stored_data

    if start_year_arg is None:
        start_year = DEFAULT_START_YEAR
    elif start_year_arg not in range(2006, 2024):
        print("Error: Start year must be between 2006 and 2022.")
        exit(1)
    else:
        start_year = start_year_arg
    
    if clear_database_arg is None:
        clear_database = DEFAULT_CLEAR_DATABASE
    elif clear_database_arg.lower() == "y":
        clear_database = True
    elif clear_database_arg.lower() == "n":
        clear_database = False
    else:
        print("Error: clear_database must be Y or N.")
        exit(1)

    if read_stored_data_arg is None:
        read_stored_data = DEFAULT_READ_STORED_DATA
    elif read_stored_data_arg.lower() == "y":
        read_stored_data = True
    elif read_stored_data_arg.lower() == "n":
        read_stored_data = False

    return start_year, clear_database, read_stored_data

def scraper(articles: bool = False, companies: bool = False, start_year: int = DEFAULT_START_YEAR):
    if not articles and not companies:
        print("Error: articles and companies can't be both false.")

    process = crawler.CrawlerProcess()
    if articles: 
        articles_class = BigArticlesSpider
        articles_class.database = database
        articles_class.startYear = str(start_year)

        process.crawl(articles_class, settings=articles_settings)
    if companies:
        companies_class = CompaniesSpider
        companies_class.database = database

        process.crawl(companies_class, settings=companies_settings)
    process.start()

def store_companies():
    with open(companies_json_file_path, 'r') as json_file:
        try:
            companies_data = json.load(json_file)
        except:
            companies_data = None
    if companies_data is None:
        print("Failed to retrieve companies data.")
        return 0
    else:
        try:
            print("Adding companies to database...")
            for company in companies_data:
                keywords = analyzer.extract_keywords(company['description'])
                tag = company['link'].split('/')[-1]
                database.addCompanytoDB(company['link'], tag, company['name'], company['description'], keywords)

            print("Successfully added companies to database.")
            return 1
        except Exception as e:
            print(f"Failed to add companies to database: {e}")
            return 0

def store_articles():
    with open(articles_json_file_path, 'r') as json_file:
        try:
            articles_data = json.load(json_file)
        except:
            articles_data = None
    if articles_data is None:
        print("Failed to retrieve articles data.")
        return 0
    else:
        try:
            print("Adding articles to database...")
            for index, article in enumerate(articles_data, start=1):
                keywords = analyzer.extract_keywords(article['text'])
                date = datetime.strptime(article['date'], "%Y-%m-%d %H:%M:%S")
                database.addArticletoDB(article['link'], article['title'], date, article['text'], article['keypoints'], article['author'], keywords)
                
                companies_names = article['companies_name'].split(', ')   
                for company_name in companies_names:
                    database.add_company_article(index, company_name)
                
            print("Successfully added articles to database.")
            return 1
        except Exception as e:
            print(f"Failed to add articles to database: {e}")
            return 0

def clear_json_files():
    try:
        with open(articles_json_file_path, 'w') as json_file:
            json_file.write("")

        with open(companies_json_file_path, 'w') as json_file:
            json_file.write("")
    except Exception as e:
        print(f"Failed to clear JSON files: {e}")
        exit(1)

def store_json_files():
    has_companies = store_companies() == 1
    has_articles = store_articles() == 1
    return has_companies, has_articles

def main():
    start_year, clear_database, read_stored_data = parse_arguments()

    if clear_database:
        print("Clearing database...")
        database.clearDatabase(drop_tables=True)         

    if read_stored_data:
        has_companies, has_articles = store_json_files()
        if not has_articles and not has_companies:
            print("Database is empty. So we need to scrape companies and articles first.")
            # scraper(articles=True, companies=True, start_year=start_year)

        elif not has_articles:
            print("Database has companies data already. So we will scrape articles only.")
            # store_companies()
            # scraper(articles=True, start_year=start_year)

        elif not has_companies:
            print("Database has articles data already. So we will scrape companies only.")
            # scraper(companies=True, start_year=start_year)
            # store_articles()
        
        else:
            print("Sucessfully retrieved companies and articles data from JSON files.")

    else:
        print("Scraping companies and articles...")
        # clear_json_files()
        # scraper(articles=True, companies=True, start_year=start_year)

if __name__ == "__main__":
    main()
