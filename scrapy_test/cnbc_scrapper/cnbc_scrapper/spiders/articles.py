import scrapy
from scrapy.exceptions import CloseSpider
from datetime import datetime
from Database import Database
from bs4 import BeautifulSoup
import re

class ArticlesSpider(scrapy.Spider):
    name = "articles"
    unique_links = set()
    database = Database("sqlite:///articles_v2_beta.db")

    def start_requests(self):
        self.database.cleanDatabase()
        urls = [
            "https://www.cnbc.com/market-insider/",
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

        link = response.css('div.LoadMore-container a::attr(href)').get()

        self.get_unique_links(response)

        if link is None:
            print(f"Retrieved {len(self.unique_links)} unique links")
            print("Now retrieving articles information...")

            for url in self.unique_links: # TODO check if this really works!!!
                yield scrapy.Request(url, callback=self.parse_articles)
        else:
            yield scrapy.Request(link, callback=self.parse)

    def parse_articles(self, response):
        # Extracting article details
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

        # We need to ensure that after a '.' there's a space, otherwise the key points will be messed up
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

        # click on load more in text (no data-link attribute, needs to use selenium - companies.py)
        more_button = response.css('div.CompanyProfile-summary div button:contains("More")')
        if more_button:
            click_action_link = more_button.css('::attr(data-link)').get()
            if click_action_link:
                full_action_url = response.urljoin(click_action_link)
                yield scrapy.Request(url=full_action_url, callback=self.parse_company_text)

    def parse_company_text(self, response):
        # get the complete text and print it
        company_description = response.css('div.CompanyProfile-descriptionContainer span::text').getall()
        complete_description = ''.join(company_description).strip()

        if complete_description:
            print(f"Complete Description: {complete_description}")

        
