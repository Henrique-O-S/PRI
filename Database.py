from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.inspection import inspect

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    date = Column(DateTime)
    text = Column(Text)
    author = Column(String)

    def __init__(self, title, date, text, author):
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

    def addArticle(self, article):
        session = self.Session()
        session.add(article)
        session.commit()
        session.close()

    def createDatabase(self):
        Base.metadata.create_all(self.engine)

    def cleanDatabase(self): #call this to delete all articles
        session = self.Session()
        session.query(Article).delete()
        session.commit()
        session.close()
