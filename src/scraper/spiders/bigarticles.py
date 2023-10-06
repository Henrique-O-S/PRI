import scrapy
from scrapy.exceptions import CloseSpider
from datetime import datetime
from bs4 import BeautifulSoup
import re

class BigArticlesSpider(scrapy.Spider):
    name = "articles"
    i = 0
    j = 0
    startYear = "2023"
    saved_items = set()
    new_items = set()
    def start_requests(self):
        self.load_saved_items()
        urls = [
            "https://www.cnbc.com/site-map/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def load_saved_items(self):
        try:
            with open("../../../articles.json", "r", encoding='utf-8') as f:
                for line in f:
                    #clean_line = unidecode(line.replace("”", "''").replace("“", "''"))
                    if line == "\n": continue
                    self.saved_items.add(line.split('"')[3])  # faster than json.loads
                print("gato")
                for i in self.saved_items:
                    print('a{}a').format(i)
                print("cao")
        except FileNotFoundError:
            scrapy.exceptions.CloseSpider("File not found. WHY")

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
        if response.url not in self.saved_items:
            self.new_items.add(response.url)
            yield {
                'article_link': response.url,
            }