import scrapy
from scrapy.exceptions import CloseSpider
from datetime import datetime
import re
from bs4 import BeautifulSoup

class BigArticlesSpider(scrapy.Spider):
    name = "articles"
    i = 0
    j = 0
    startYear = "2023"
    def start_requests(self):
        urls = [
            "https://www.cnbc.com/site-map/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if response.status != 200:
            print(f"Failed to retrieve content. Status code: {response.status}")
            raise CloseSpider("Failed to retrieve content")

        yearsUrl = response.css('div.SiteMapYear-yearData a::attr(href)').getall()

        for yearUrl in yearsUrl:
            if yearUrl.split("/")[-2] >= self.startYear:
                yield scrapy.Request(url='https:' + yearUrl, callback=self.parse_year)


    def parse_year(self, response):
        if response.status != 200:
            print(f"Failed to retrieve content. Status code: {response.status}")
            raise CloseSpider("Failed to retrieve content")

        monthsUrl = response.css('div.SiteMapMonth-monthData a::attr(href)').getall()

        for monthUrl in monthsUrl:
            yield scrapy.Request(url='https:' + monthUrl, callback=self.parse_month)

    def parse_month(self, response):
        if response.status != 200:
            print(f"Failed to retrieve content. Status code: {response.status}")
            raise CloseSpider("Failed to retrieve content")

        daysUrl = response.css('div.SiteMapDay-fullDate a::attr(href)').getall()

        for dayUrl in daysUrl:
            yield scrapy.Request(url='https:' + dayUrl, callback=self.parse_day)

    def parse_day(self, response):
        if response.status != 200:
            print(f"Failed to retrieve content. Status code: {response.status}")
            raise CloseSpider("Failed to retrieve content")

        articlesUrl = response.css('div.SiteMapArticleList-articleData a::attr(href)').getall()
        for articleUrl in articlesUrl:
            self.j+=1
            if articleUrl.split("/")[-1].startswith("stocks"):
                self.i+=1
                yield scrapy.Request(url=articleUrl, callback=self.check_article)

        print(f"Found {self.i} articles about stocks out of {self.j} articles")

    def check_article(self, response):
        if response.status != 200:
            print(f"Failed to retrieve content. Status code: {response.status}")
            raise CloseSpider("Failed to retrieve content")

        category = response.css('a.ArticleHeader-eyebrow::text').get()
        if category is None:
            category = response.css('a.ArticleHeader-styles-makeit-eyebrow--Degp4::text').get()
        if category != "Market Insider":
            return # because its a paid article or not market insider category
        if response.url not in self.database.saved_urls:
            print(f"Found article: {response.url}")
            
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

            text = re.sub(r'—', '-', text)

            try:
                text.encode("windows-1252").decode("utf-8")
            except UnicodeEncodeError:
                text = text.encode("utf-8").decode("utf-8")

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

            ## Deal with companies...
            

            yield {
                'link': response.url,
                'title': title,
                'date': date,
                'text': text,
                'keypoints': key_points_text,
                'author': author
                # 'companies_name': companies
            }
        else:
            print(f"Article already saved: {response.url}")
