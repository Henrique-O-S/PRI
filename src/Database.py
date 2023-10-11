from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.inspection import inspect
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class CompanyArticleAssociation(Base):
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
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    link = Column(Text)
    title = Column(String)
    date = Column(DateTime)
    text = Column(Text)
    keypoints = Column(Text)
    author = Column(String)
    keywords = Column(Text)
    companies = relationship('Company', secondary=CompanyArticleAssociation.__table__, back_populates='articles')

    def __init__(self, link, title, date, text, keypoints, author, keywords=''):
        self.link = link
        self.title = title
        self.date = date
        self.text = text
        self.keypoints = keypoints
        self.author = author
        self.keywords = keywords

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    link = Column(Text)
    tag = Column(String)
    name = Column(String)
    description = Column(Text)
    keywords = Column(Text)
    articles = relationship('Article', secondary=CompanyArticleAssociation.__table__, back_populates='companies')

    def __init__(self, link, tag, name, description, keywords=''):
        self.link = link
        self.tag = tag
        self.name = name
        self.description = description
        self.keywords = keywords

class Database:
    saved_urls = set()
    def __init__(self, db_file = "sqlite:///data/articles.db"):
        self.db_file = db_file
        self.engine = create_engine(self.db_file)
        self.Session = sessionmaker(bind=self.engine)

        if not inspect(self.engine).has_table(Article.__tablename__) or not inspect(self.engine).has_table(
                Company.__tablename__):
            self.createDatabase()
        
        self.__store_articles_url()

    def __store_articles_url(self):
        session = self.Session()
        articles = session.query(Article).all()
        for article in articles:
            self.saved_urls.add(article.link)
        session.close()
            
    def addArticletoDB(self, articleUrl, title, date, text, keypoints, author, keywords=None):
        session = self.Session()
        session.add(Article(articleUrl, title, date, text, keypoints, author, keywords))
        session.commit()
        session.close()
        self.saved_urls.add(articleUrl)

    def addCompanytoDB(self, link, tag, name, description, keywords=None):
        try:
            session = self.Session()
            existing_company = session.query(Company).filter_by(name=name).first()
            if not existing_company:
                session.add(Company(link, tag, name, description, keywords))
            session.commit()
        except Exception as e:
            print(f"Failed to add company {name} to database: {e}")
        finally:
            session.close()

    def add_company_article(self, article_id, company_tag):
        session = self.Session()
        company = session.query(Company).filter(Company.tag.like(f"%{company_tag}%")).first()
        if company:
            association = CompanyArticleAssociation(company_id=company.id, article_id=article_id)
            session.add(association)
            session.commit()
        session.close()

    def createDatabase(self):
        Base.metadata.create_all(self.engine)

    def clearDatabase(self): 
        session = self.Session()
        session.query(CompanyArticleAssociation).delete()
        session.query(Article).delete()
        session.query(Company).delete()
        session.commit()
        session.close()

        self.saved_urls.clear()
