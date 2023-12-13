from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.inspection import inspect
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import re

Base = declarative_base()

class CompanyArticleAssociation(Base):
    """
    Define a many-to-many relationship between Companies and Articles.
    
    Columns:
    - id: the id of the association
    - company_id: the id of the company
    - article_id: the id of the article
    """

    __tablename__ = "company_article_association"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'))
    article_id = Column(Integer, ForeignKey('articles.id'))
    company = relationship("Company", backref="company_article_associations")
    article = relationship("Article", backref="article_company_associations")

    def __init__(self, company_id, article_id):
        self.company_id = company_id
        self.article_id = article_id

class Article(Base):
    """
    Define the Article table.
    
    Columns:
    - link: the link to the article
    - title: the title of the article
    - date: the date of the article
    - text: the text of the article
    - keypoints: the keypoints of the article
    - author: the author('s) of the article
    - keywords: the keywords extracted from the text
    """

    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    link = Column(Text)
    title = Column(String)
    date = Column(DateTime)
    text = Column(Text)
    keypoints = Column(Text)
    author = Column(String)
    keywords = Column(Text)
    #companies = relationship('Company', secondary=CompanyArticleAssociation.__table__, back_populates='articles')

    def __init__(self, link, title, date, text, keypoints, author, keywords=''):
        self.link = link
        self.title = title
        self.date = date
        self.text = text
        self.keypoints = keypoints
        self.author = author
        self.keywords = keywords

class Company(Base):
    """
    Define the Company table.
    
    Columns:
    - link: the link to the company's page on CNBC
    - tag: the tag of the company (e.g. AAPL for Apple)
    - name: the name of the company
    - description: the description of the company
    - keywords: the keywords extracted from the description
    """

    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    link = Column(Text)
    tag = Column(String)
    name = Column(String)
    description = Column(Text)
    keywords = Column(Text)
    #articles = relationship('Article', secondary=CompanyArticleAssociation.__table__, back_populates='companies')

    def __init__(self, link, tag, name, description, keywords=''):
        self.link = link
        self.tag = tag
        self.name = name
        self.description = description
        self.keywords = keywords

class Database:
    """
    Define the Database class.

    Attributes:
    - db_file: the path to the database file
    - engine: the database engine
    - Session: the database session
    - saved_urls: the set of saved article urls
    - saved_companies_urls: the set of saved company urls

    Private methods:

    - __store_articles_url: store article urls in a set
    - __store_companies_url: store company urls in a set
    - __dropAllTables: drop all tables in the database

    Public methods to add data to the database.

    Methods:
    - addArticletoDB: add an article to the database
    - addCompanytoDB: add a company to the database
    - add_company_article: add a company-article association to the database
    - createDatabase: create the database
    - clearDatabase: clear the database
    - has_data: check if the database has data
    """

    saved_urls = set()
    saved_companies_urls = set()

    def __init__(self, db_file : str = "sqlite:///data/articles.db", clear : bool = False):
        self.db_file = db_file
        self.engine = create_engine(self.db_file)
        self.Session = sessionmaker(bind=self.engine)

        try:
            if clear:
                self.clearDatabase(drop_tables=True)
            self.createDatabase()
            self.__store_articles_url()
            self.__store_companies_url()
        except Exception as e:
            print(f"Database initialization failed: {e}")

    # Private method to store article URLs in a set
    def __store_articles_url(self) -> None:
        session = self.Session()
        try:
            articles = session.query(Article).all()
            for article in articles:
                self.saved_urls.add(article.link)
        except Exception as e:
            print(f"Failed to store article URLs: {e}")
        finally:
            session.close()

    # Private method to store company URLs in a set
    def __store_companies_url(self) -> None:
        session = self.Session()
        try:
            companies = session.query(Company).all()
            for company in companies:
                self.saved_companies_urls.add(company.link)
        except Exception as e:
            print(f"Failed to store company URLs: {e}")
        finally:
            session.close()
    # Private method to drop all tables in the database
    def __dropAllTables(self) -> None:
        insp = inspect(self.engine)
        if insp.has_table(Article.__tablename__):
            Article.__table__.drop(self.engine)
        if insp.has_table(Company.__tablename__):
            Company.__table__.drop(self.engine)
        if insp.has_table(CompanyArticleAssociation.__tablename__):
            CompanyArticleAssociation.__table__.drop(self.engine)
    
    # Public method to add an article to the database
    def addArticletoDB(self, articleUrl : str, title : str, date : datetime, text : str, keypoints : str, author : str, keywords=None) -> None:
        session = self.Session()
        try:
            session.add(Article(articleUrl, title, date, text, keypoints, author, keywords))
            session.commit()
            self.saved_urls.add(articleUrl)
        except Exception as e:
            session.rollback()
            print(f"Failed to add article to database: {e}")
        finally:
            session.close()

    # Public method to add a company to the database
    def addCompanytoDB(self, link : str, tag : str, name : str, description : str, keywords : str = None) -> None:
        session = self.Session()
        try:
            existing_company = session.query(Company).filter_by(name=name).first()
            if not existing_company:
                session.add(Company(link, tag, name, description, keywords))
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Failed to add company to database: {e}")
        finally:
            session.close()

    # Public method to add a company-article association to the database
    def add_company_article(self, article_id: str, company_tag: str) -> None:
        session = self.Session()
        try:
            company = session.query(Company).filter(Company.tag.like(f"%{company_tag}%")).first()
            if company:
                association = CompanyArticleAssociation(company_id=company.id, article_id=article_id)
                session.add(association)
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Failed to add company-article association to the database: {e}")
        finally:
            session.close()


    # Public method to create the database
    def createDatabase(self) -> None:
        try:
            if not inspect(self.engine).has_table(Article.__tablename__) \
                    or not inspect(self.engine).has_table(Company.__tablename__) \
                    or not inspect(self.engine).has_table(CompanyArticleAssociation.__tablename__):
                Base.metadata.create_all(self.engine)
        except Exception as e:
            print(f"Failed to create database: {e}")

    # Public method to clear the database
    def clearDatabase(self, drop_tables : bool = False): 
        session = self.Session()
        try:
            session.query(CompanyArticleAssociation).delete()
            session.query(Article).delete()
            session.query(Company).delete()
            session.commit()
            self.saved_urls.clear()
            self.saved_companies_urls.clear()
            if drop_tables:
                self.__dropAllTables()
        except Exception as e:
            session.rollback()
            print(f"Failed to clear database: {e}")
        finally:
            session.close()

    # Public method to check if the database has data
    def has_data(self) -> tuple:
        has_articles = len(self.saved_urls) != 0
        has_companies = len(self.saved_companies_urls) != 0
        return has_articles, has_companies

    # Public method to get all associations between companies and articles
    def get_all_company_article_associations(self):
        session = self.Session()
        associations = session.query(CompanyArticleAssociation).all()
        session.close()
        return associations

    # Public method to get all articles
    def get_all_articles(self):
        session = self.Session()
        articles = session.query(Article).all()
        for article in articles:
            text = article.text.replace("Â", "-")
            article.text = re.sub(r'\.(\s+)(\d)', r'.\2', text)
        session.close()
        return articles

    # Public method to get all companies
    def get_all_companies(self):
        session = self.Session()
        companies = session.query(Company).all()
        session.close()
        return companies
    
    def get_article_companies(self, article_id):
        session = self.Session()
        try:
            associations = session.query(CompanyArticleAssociation).filter_by(article_id=article_id).all()
            company_ids = [association.company_id for association in associations]
            companies = session.query(Company).filter(Company.id.in_(company_ids)).all()
            session.close()
            return companies
        except Exception as e:
            print(f"Failed to get article companies: {e}")
            session.close()
            return []
        
    def get_tesla_mentions(self):
        session = self.Session()
        try:
            tesla_articles_dates = session.query(Article.date).\
                join(CompanyArticleAssociation, Article.id == CompanyArticleAssociation.article_id).\
                join(Company, Company.id == CompanyArticleAssociation.company_id).\
                filter(Company.tag == "TSLA").all()
            return tesla_articles_dates
        except Exception as e:
            print(f"Failed to run query: {e}")
            return None
        finally:
            session.close()