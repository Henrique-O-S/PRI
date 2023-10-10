import json
from src.Database import Database
from src.analyzer import Analyzer

with open('companies.json', 'r') as json_file:
    companies_data = json.load(json_file)

database = Database()
analyzer = Analyzer()
for company in companies_data:
    keywords = analyzer.extract_keywords(company['description'])
    database.addCompanytoDB(company['link'], company['name'], company['description'], keywords)