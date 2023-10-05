import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.inspection import inspect

from datetime import datetime

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

    def __init__(self, name, stock_price, description):
        self.name = name
        self.stock_price = stock_price
        self.description = description

class Database:
    def __init__(self, db_file = "sqlite:///data/articles.db"):
        self.db_file = db_file
        self.engine = create_engine(self.db_file)
        self.Session = sessionmaker(bind=self.engine)

        if not inspect(self.engine).has_table(Article.__tablename__) or not inspect(self.engine).has_table(Company.__tablename__):
            self.createDatabase()

    def addArticletoDB(self, articleUrl, title, date, text, keypoints, author):
        session = self.Session()
        session.add(Article(articleUrl, title, date, text, keypoints, author))
        session.commit()
        session.close()

    def addCompanytoDB(self, name, stock_price, description):
        session = self.Session()
        existing_company = session.query(Company).filter_by(name=name).first()
        if not existing_company:
            session.add(Company(name, stock_price, description))
        session.commit()
        session.close()

    def addArticle(self, articleUrl):
        response = requests.get(articleUrl)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the response using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            title = soup.find('h1', class_='ArticleHeader-headline')
            if title is None:
                title = soup.find('h1', class_='ArticleHeader-styles-makeit-headline--l_iUX')
            article = soup.find('div', class_='ArticleBody-articleBody')
            if article is None:
                article = soup.find('div', class_='ArticleBody-styles-makeit-articleBody--AEqcE')
            textdivs = article.find_all('div', class_='group')
            text = ""
            for textdiv in textdivs:
                text += textdiv.get_text()
                
            key_points_text =""
            key_points_list = soup.find('div', class_='RenderKeyPoints-list')
            if key_points_list is None:
                pass
            else:
                key_points_ul = key_points_list.find('div').find('div').find('ul')
                key_points = key_points_ul.find_all('li')
                for key_point in key_points:
                    key_points_text += key_point.text
                print(key_points_text)

            date = soup.find('time', attrs={"data-testid": "lastpublished-timestamp"})
            if date is None:
                date = soup.find('time', attrs={"data-testid": "published-timestamp"})

            author=""
            authorsA = soup.find_all('a', class_='Author-authorName')
            for authorA in authorsA:
                author += (authorA.get_text() + ",")

            self.addArticletoDB(articleUrl, title.text, datetime.strptime(date.get("datetime"), "%Y-%m-%dT%H:%M:%S%z"), text, key_points_text, author[:-1])

    def createDatabase(self):
        Base.metadata.create_all(self.engine)

    def clearDatabase(self): #call this to delete all data
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

    def populateDatabase(self):
        self.clearDatabase()

        articlesURL = self.retrieveAllArticlesURL(starting_url="https://www.cnbc.com/market-insider/")
        for link in articlesURL:
            self.addArticle(link)
            print(link)
