import scrapy
from scrapy.exceptions import CloseSpider
from datetime import datetime
from src.Database import Database
from bs4 import BeautifulSoup
import re

class ArticlesSpider(scrapy.Spider):
    name = "articles"
    links_to_save = set()
    database = Database()

    def load_saved_items(self):
        try:
            with open("../../../articles.json", "r", encoding='utf-8') as f:
                for line in f:
                    #clean_line = unidecode(line.replace("”", "''").replace("“", "''"))
                    if line == "\n": continue
                    self.links_to_save.add(line.split('"')[3])  # faster than json.loads
        except FileNotFoundError:
            scrapy.exceptions.CloseSpider("File not found. WHY")
    def start_requests(self):
        self.load_saved_items()

        for url in self.links_to_save:
            yield scrapy.Request(url=url, callback=self.parsearticle)

    def get_unique_links(self, response):
        for div_tag in response.css('div'):
            if len(div_tag.css('a')) == 1:
                href = div_tag.css('a::attr(href)').get()
                if href and href.startswith("https://www.cnbc.com/20"):
                    self.unique_links.add(href)

    def parse_article(self, response):
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

    def parse_companies(self, response):
        company_name = response.css('h1.QuoteStrip-quoteTitle span.QuoteStrip-name::text').get()
        if company_name:
            print(f"Company Name: {company_name}")

        company_stock_price = response.css('div.QuoteStrip-lastPriceStripContainer span.QuoteStrip-lastPrice::text').get()
        if company_stock_price:
            print(f"Company Stock Price: {company_stock_price}")

        company_description = response.css('div.CompanyProfile-summary span::text').getall()
        complete_description = ''.join(company_description).strip()
        if complete_description:
            print(f"Company Description: {complete_description}")

        self.database.addCompanytoDB(company_name, company_stock_price, complete_description)
