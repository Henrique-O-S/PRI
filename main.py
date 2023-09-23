
import requests
from bs4 import BeautifulSoup

from Database import Database, Article
from datetime import date


if __name__ == "__main__":
    database = Database("sqlite:///articles.db")
    database.addArticle(Article("name", date.today(), "text", "author"))

def fetchLinks():
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
    else:
        print(f"Failed to retrieve content. Status code: {response.status_code}")
