import scrapy
from scrapy.exceptions import CloseSpider
from datetime import datetime
import re
from bs4 import BeautifulSoup
import logging

class BigArticlesSpider(scrapy.Spider):
    """
    Scrapes articles from CNBC.

    Attributes:
        name: The name of the spider.
        startYear: The starting year. Default is 2023.
        database: The database to store the scraped data. This is passed in from the caller.

    Methods:
        start_requests: Creates a request to the CNBC article list.
        parse: Parses the article list page.
        parse_year: Parses the year from the article list page.
        parse_month: Parses the month from the article list page.
        parse_day: Parses the day from the article list page.
        parse_article: Parses the article from the article page.
        check_article: Checks if the article is a market insider article.
    """
    name = "articles"
    startYear = "2023"

    def start_requests(self):
        # Cnbc article list entrypoint
        yield scrapy.Request(url="https://www.cnbc.com/site-map/", callback=self.parse)

    def parse(self, response):
        if response.status != 200:
            logging.error(f"Failed to retrieve content. Status code: {response.status}")
            raise CloseSpider("Failed to retrieve content")

        # Retrieve the urls for the years
        yearsUrl = response.css('div.SiteMapYear-yearData a::attr(href)').getall()

        for yearUrl in yearsUrl:
            if yearUrl.split("/")[-2] >= self.startYear:
                yield scrapy.Request(url='https:' + yearUrl, callback=self.parse_year)


    def parse_year(self, response):
        if response.status != 200:
            logging.error(f"Failed to retrieve content. Status code: {response.status}")
            raise CloseSpider("Failed to retrieve content")

        # Retrieve the urls for the months
        monthsUrl = response.css('div.SiteMapMonth-monthData a::attr(href)').getall()

        for monthUrl in monthsUrl:
            yield scrapy.Request(url='https:' + monthUrl, callback=self.parse_month)

    def parse_month(self, response):
        if response.status != 200:
            logging.error(f"Failed to retrieve content. Status code: {response.status}")
            raise CloseSpider("Failed to retrieve content")

        # Retrieve the urls for the days
        daysUrl = response.css('div.SiteMapDay-fullDate a::attr(href)').getall()

        for dayUrl in daysUrl:
            yield scrapy.Request(url='https:' + dayUrl, callback=self.parse_day)

    def parse_day(self, response):
        if response.status != 200:
            logging.error(f"Failed to retrieve content. Status code: {response.status}")
            raise CloseSpider("Failed to retrieve content")

        # Retrieve the urls for the articles themselfs
        articlesUrl = response.css('div.SiteMapArticleList-articleData a::attr(href)').getall()
        for articleUrl in articlesUrl:
            if articleUrl in self.database.saved_urls: 
                logging.warning(f"Article already saved: {articleUrl}")
                continue

            print(f"Found new article: {articleUrl}")
            if articleUrl.split("/")[-1].startswith("stocks"):
                yield scrapy.Request(url=articleUrl, callback=self.check_article)

    def check_article(self, response):
        if response.status != 200:
            logging.error(f"Failed to retrieve content. Status code: {response.status}")
            raise CloseSpider("Failed to retrieve content")

        # Check if the article is a market insider article
        category = response.css('a.ArticleHeader-eyebrow::text').get()
        if category is None:
            category = response.css('a.ArticleHeader-styles-makeit-eyebrow--Degp4::text').get()
        if category != "Market Insider":
            return # because its a paid article or not market insider category
        
        # Extracting article details
        title = response.css('h1.ArticleHeader-headline::text, h1.ArticleHeader-styles-makeit-headline--l_iUX::text').get()

        # We need to get the text from the article, it's only possible with bs4 without shenanigans
        soup = BeautifulSoup(response.text, 'html.parser')
        article = soup.find('div', class_='ArticleBody-articleBody')
        if article is None:
            article = soup.find('div', class_='ArticleBody-styles-makeit-articleBody--AEqcE')
        textdivs = article.find_all('div', class_='group')
        text = ""
        for textdiv in textdivs:
            text += textdiv.get_text()

        # We need to ensure that after a '.' there's a space, otherwise the key points will be messed up
        text = re.sub(r'\.(?!\s)', '. ', text)

        # Replace em dash with hyphen
        text = re.sub(r'—', '-', text) 

        # Replace non-breaking space with space
        try:
            text = text.replace("\xa0", " ").encode("windows-1252").decode("ISO-8859-1")
        except UnicodeEncodeError:
            logging.error("Failed to encode text")

        # Retrieve the key points if they exist
        key_points_list = response.css('div.RenderKeyPoints-list')
        key_points_text = ""
        if key_points_list:
            key_points = key_points_list.css('ul li::text').getall()
            key_points_text = ''.join(key_points)

        # Retrieve the date if it exists
        date_tag = response.css('time[data-testid="lastpublished-timestamp"], time[data-testid="published-timestamp"]')
        date = datetime.strptime(date_tag.attrib["datetime"], "%Y-%m-%dT%H:%M:%S%z") if date_tag else None

        # Retrieve the author if it exists
        authors = response.css('a.Author-authorName::text').getall()
        author = ','.join(authors)

        print(f"Retrieved article: Title - {title}, Date - {date}")

        companies = []

        # Get companies from the article text if they exist
        href_links = [link['href'] for textdiv in textdivs for link in textdiv.find_all('a', href=True)]
        href_links = [link for link in href_links if link.startswith('/quotes/')]
        for link in href_links:
            companies.append(link.split('/')[-2])

        companies = ", ".join(companies)
        

        yield {
            'link': response.url,
            'title': title,
            'date': date,
            'text': text,
            'keypoints': key_points_text,
            'author': author,
            'companies_name': companies
        }
