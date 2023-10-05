import scrapy
from scrapy.exceptions import CloseSpider
from datetime import datetime
from src.Database import Database
from bs4 import BeautifulSoup
import re

class BigArticlesSpider(scrapy.Spider):
    name = "articles"
    unique_links = set()
    database = Database()
    i = 0
    j = 0
    startYear = "2019"

    def start_requests(self):
        #self.database.clearDatabase()
        urls = [
            "https://www.cnbc.com/site-map/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def get_unique_links(self, response):
        for div_tag in response.css('div'):
            if len(div_tag.css('a')) == 1:
                href = div_tag.css('a::attr(href)').get()
                if href and href.startswith("https://www.cnbc.com/20"):
                    self.unique_links.add(href)

    def parse(self, response):
        if response.status != 200:
            print(f"Failed to retrieve content. Status code: {response.status}")
            raise CloseSpider("Failed to retrieve content")

        yearsUrl = response.css('div.SiteMapYear-yearData a::attr(href)').getall()

        for yearUrl in yearsUrl:
            #print(yearUrl)
            if yearUrl.split("/")[-2] >= self.startYear:
                yield scrapy.Request(url='https:' + yearUrl, callback=self.parseYear)


    def parseYear(self, response):
        if response.status != 200:
            print(f"Failed to retrieve content. Status code: {response.status}")
            raise CloseSpider("Failed to retrieve content")

        monthsUrl = response.css('div.SiteMapMonth-monthData a::attr(href)').getall()

        for monthUrl in monthsUrl:
            #print(monthUrl)
            yield scrapy.Request(url='https:' + monthUrl, callback=self.parseMonth)

    def parseMonth(self, response):
        if response.status != 200:
            print(f"Failed to retrieve content. Status code: {response.status}")
            raise CloseSpider("Failed to retrieve content")

        daysUrl = response.css('div.SiteMapDay-fullDate a::attr(href)').getall()

        for dayUrl in daysUrl:
            #print(dayUrl)
            yield scrapy.Request(url='https:' + dayUrl, callback=self.parseDay)

    def parseDay(self, response):
        if response.status != 200:
            print(f"Failed to retrieve content. Status code: {response.status}")
            raise CloseSpider("Failed to retrieve content")

        articlesUrl = response.css('div.SiteMapArticleList-articleData a::attr(href)').getall()
        for articleUrl in articlesUrl:
            self.j+=1
            if articleUrl.split("/")[-1].startswith("stocks"):
                self.i+=1
        print(f"Found {self.i} articles about stocks out of {self.j} articles")
    def parse_articles(self, response):
        # extracting article details
        title = response.css('h1.ArticleHeader-headline::text, h1.ArticleHeader-styles-makeit-headline--l_iUX::text').get()

        # we need to get the text from the article, it's only possible with bs4 without shenanigans
        soup = BeautifulSoup(response.text, 'html.parser')
        article = soup.find('div', class_='ArticleBody-articleBody')
        if article is None:
            article = soup.find('div', class_='ArticleBody-styles-makeit-articleBody--AEqcE')
        textdivs = article.find_all('div', class_='group')
        text = ""
        for textdiv in textdivs:
            text += textdiv.get_text()

        # we need to ensure that after a '.' there's a space, otherwise the key points will be messed up
        text = re.sub(r'\.(?!\s)', '. ', text)
        
        key_points_list = response.css('div.RenderKeyPoints-list')
        key_points_text = ""
        if key_points_list:
            key_points = key_points_list.css('ul li::text').getall()
            key_points_text = ''.join(key_points)

        date_tag = response.css('time[data-testid="lastpublished-timestamp"], time[data-testid="published-timestamp"]')
        date = datetime.strptime(date_tag.attrib["datetime"], "%Y-%m-%dT%H:%M:%S%z") if date_tag else None
        
        authors = response.css('a.Author-authorName::text').getall()
        author = ','.join(authors)

        print(f"Retrieved article: Title - {title}, Date - {date}")

        self.database.addArticletoDB(response.url, title, date, text, key_points_text, author)

        company_links = response.css('a[href^="/quotes/"]::attr(href)').getall()
        for company_link in company_links:
            company_url = response.urljoin(company_link)
            yield scrapy.Request(url=company_url, callback=self.parse_companies)

