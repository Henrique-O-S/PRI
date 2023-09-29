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
    category = Column(Text)
    title = Column(String)
    date = Column(DateTime)
    text = Column(Text)
    author = Column(String)

    def __init__(self, link, category, title, date, text, author):
        self.link = link
        self.category = category
        self.title = title
        self.date = date
        self.text = text
        self.author = author

class Database:
    def __init__(self, url):
        self.url = url
        self.engine = create_engine(self.url)
        self.Session = sessionmaker(bind=self.engine)

        if not inspect(self.engine).has_table(Article.__tablename__):
            self.createDatabase()
    def addArticle(self, articleUrl):
        response = requests.get(articleUrl)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the response using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            article = soup.find('div', class_='ArticleBody-articleBody')
            if article is None:
                article = soup.find('div', class_='ArticleBody-styles-makeit-articleBody--AEqcE')
            textdivs = article.find_all('div', class_='group')
            title = soup.find('h1', class_='ArticleHeader-headline')
            if title is None:
                title = soup.find('h1', class_='ArticleHeader-styles-makeit-headline--l_iUX')
            key_points_text =[]
            key_points_list = soup.find('div', class_='RenderKeyPoints-list')
            if key_points_list is None:
                pass
            else:
                key_points_ul = key_points_list.find('div').find('div').find('ul')
                key_points = key_points_ul.find_all('li')
                for key_point in key_points:
                    key_points_text.append(key_point.text)
                    print(key_point.text)
            text = ""
            for textdiv in textdivs:
                text += textdiv.get_text()
            print(text)
            print(title.text)
            date = soup.find('time', attrs={"data-testid": "lastpublished-timestamp"})
            if date is None:
                date = soup.find('time', attrs={"data-testid": "published-timestamp"})

            print(date.get("datetime"))
            author=""
            authorsA = soup.find_all('a', class_='Author-authorName')
            for authorA in authorsA:
                author += (authorA.get_text() + ",")

            type = soup.find('a', class_='ArticleHeader-eyebrow')
            if type is None:
                type = soup.find('a', class_='ArticleHeader-styles-makeit-eyebrow--Degp4')
            session = self.Session()
            session.add(Article(articleUrl, type.text, title.text, datetime.strptime(date.get("datetime"), "%Y-%m-%dT%H:%M:%S%z"), text, author[:-1]))
            session.commit()
            session.close()

    def createDatabase(self):
        Base.metadata.create_all(self.engine)

    def cleanDatabase(self): #call this to delete all articles
        session = self.Session()
        session.query(Article).delete()
        session.commit()
        session.close()

    def populateDatabase(self):
        self.cleanDatabase()
        url = "https://www.cnbc.com/finance/"

        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            unique_links = set()

            for div_tag in soup.find_all('div'):
                if len(div_tag.find_all()) == 1 and div_tag.find('a'):
                    href = div_tag.find('a').get('href')
                    if href and href.startswith("https://www.cnbc.com/20"):
                        unique_links.add(href)

            for link in unique_links:
                print(link)
                self.addArticle(link)
        else:
            print(f"Failed to retrieve content. Status code: {response.status_code}")
