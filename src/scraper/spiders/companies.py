import scrapy
from scrapy.exceptions import CloseSpider
from src.Database import Database
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from ...analyzer import Analyzer

class CompaniesSpider(scrapy.Spider):
    def __init__(self):
        self.name = "companies"
        self.unique_links = set()
        self.database = Database("sqlite:///stonks.db")
        self.driver = webdriver.Chrome()
        self.analyzer = Analyzer()

    def start_requests(self):
        self.database.clearDatabase()
        urls = [
            "https://www.cnbc.com/nasdaq-100/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def get_unique_links(self, response):
        self.driver.get(response.url)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href^="//www.cnbc.com/quotes/"]'))
        )
        company_links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href^="//www.cnbc.com/quotes/"]')

        for link in company_links:
            company_link = link.get_attribute("href")
            self.unique_links.add(company_link)

    def parse(self, response):
        if response.status != 200:
            print(f"Failed to retrieve content. Status code: {response.status}")
            raise CloseSpider("Failed to retrieve content")

        self.get_unique_links(response)
        print(f"Retrieved {len(self.unique_links)} unique links")
        print("Now retrieving companies data...")

        accept_cookies_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        accept_cookies_button.click()

        for url in self.unique_links:
            yield scrapy.Request(url, callback=self.parse_company)

    def parse_company(self, response):
        if response.status != 200:
            print(f"Failed to retrieve content. Status code: {response.status}")
            raise CloseSpider("Failed to retrieve content")
        
        company_name = response.css('h1.QuoteStrip-quoteTitle span.QuoteStrip-name::text').get()
        company_stock_price = response.css('div.QuoteStrip-lastPriceStripContainer span.QuoteStrip-lastPrice::text').get()

        self.driver.get(response.url)
        try:
            more_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='More']"))
            )
            actions = ActionChains(self.driver)
            actions.move_to_element(more_button).perform()
            more_button.click()
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.CompanyProfile-summary span"))
            )
            company_description = self.driver.find_element(By.CSS_SELECTOR, "div.CompanyProfile-summary span").text
            company_description = company_description.strip()
            company_keywords = self.analyzer.extract_keywords(company_description)
            self.database.addCompanytoDB(company_name, company_stock_price, company_description, company_keywords)
        except StaleElementReferenceException:
            print("ERROR: Element is stale.")

    def closed(self, reason):
        self.driver.quit()  