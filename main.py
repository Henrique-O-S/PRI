
import requests
from bs4 import BeautifulSoup

from Database import Database, Article
from datetime import date


if __name__ == "__main__":
    database = Database("sqlite:///articles.db")
    #database.populateDatabase()