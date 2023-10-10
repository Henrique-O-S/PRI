from sqlite3 import OperationalError

import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.inspection import inspect
import json
import os

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    link = Column(Text)
    title = Column(String)
    date = Column(DateTime)
    text = Column(Text)
    keypoints = Column(Text)
    author = Column(String)

    def __init__(self, link, title, date, text, keypoints, author):
        self.link = link
        self.title = title
        self.date = date
        self.text = text
        self.keypoints = keypoints
        self.author = author

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    stock_price = Column(String)
    description = Column(Text)
    keywords = Column(Text)

    def __init__(self, name, stock_price, description, keywords=None):
        self.name = name
        self.stock_price = stock_price
        self.description = description
        self.keywords = keywords

class Database:
    saved_items = set()
    links_to_save = set()
    def __init__(self, db_file = "sqlite:///data/articles.db"):
        self.db_file = db_file
        self.engine = create_engine(self.db_file)
        self.Session = sessionmaker(bind=self.engine)

        if not inspect(self.engine).has_table(Article.__tablename__) or not inspect(self.engine).has_table(
                Company.__tablename__):
            self.createDatabase()
        self.load_saved_items()
        self.load_items_to_save()

    def addArticletoDB(self, articleUrl, title, date, text, keypoints, author):
        session = self.Session()
        session.add(Article(articleUrl, title, date, text, keypoints, author))
        session.commit()
        session.close()

    def addCompanytoDB(self, name, stock_price, description, keywords=None):
        session = self.Session()
        existing_company = session.query(Company).filter_by(name=name).first()
        if not existing_company:
            session.add(Company(name, stock_price, description, keywords))
        session.commit()
        session.close()

    def createDatabase(self):
        Base.metadata.create_all(self.engine)

    def clearDatabase(self): 
        session = self.Session()
        session.query(Article).delete()
        session.query(Company).delete()
        session.commit()
        session.close()

    def retrieveAllArticlesURL(self, starting_url):
        response = requests.get(starting_url)

        unique_links = set()

        while response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            articles = soup.find_all('div', class_='PageBuilder-col-9 PageBuilder-col')
            for article in articles:
                for div_tag in article.find_all('div'):
                    if len(div_tag.find_all()) == 1 and div_tag.find('a'):
                        href = div_tag.find('a').get('href')
                        if href and href.startswith("https://www.cnbc.com/20"):
                            unique_links.add(href)

            next_page = soup.find('a', class_='LoadMoreButton-loadMore')

            if next_page:
                next_page_url = next_page.get('href')
                response = requests.get(next_page_url)
                print(f"Retrieving {next_page_url}")
            else: 
                break

        else:
            print(f"Failed to retrieve content. Status code: {response.status_code}")

        return unique_links

    def load_saved_items(self):
        current_directory = os.getcwd()
        file_path = os.path.join(current_directory, "saved_links.json")
        try:
            with open(file_path, "r", encoding='utf-8') as f:
                file_content = f.read()
                if file_content.strip():
                    data = json.loads(file_content)
                    for item in data:
                        self.saved_items.add(item['article_link'])
                else:
                    print("The JSON file is empty.")
        except FileNotFoundError:
            print("FILE NOT FOUND")

    def load_items_to_save(self):
        current_directory = os.getcwd()
        file_path = os.path.join(current_directory, "links_to_save.json")
        try:
            with open(file_path, "r", encoding='utf-8') as f:
                file_content = f.read()
                if file_content.strip():
                    data = json.loads(file_content)
                    for item in data:
                        self.links_to_save.add(item['article_link'])
                else:
                    print("The JSON file is empty.")
        except FileNotFoundError:
            print("FILE NOT FOUND")
