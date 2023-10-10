import scrapy
from scrapy.exceptions import CloseSpider
from src.Database import Database
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class CompaniesSpider(scrapy.Spider):
    def __init__(self):
        # init variables
        self.name = "companies"
        self.unique_links = set()
        self.database = Database()
        self.driver = webdriver.Chrome()

    def start_requests(self):
        # cnbc company list
        yield scrapy.Request(url="https://www.cnbc.com/nasdaq-100/", callback=self.parse)

    def parse(self, response):
        # check response
        if response.status != 200:
            print(f"Failed to retrieve content. Status code: {response.status}")
            raise CloseSpider("Failed to retrieve content")
        # get company links
        self.driver.get(response.url)
        self.parse_links()
        # accept cookies
        accept_cookies_button = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        accept_cookies_button.click()
        # parse company pages
        for url in self.unique_links:
            yield scrapy.Request(url, callback=self.parse_company)

    def parse_links(self):
        # wait for links to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href^="//www.cnbc.com/quotes/"]'))
        )
        company_links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href^="//www.cnbc.com/quotes/"]')
        # store links
        for link in company_links:
            company_link = link.get_attribute("href")
            self.unique_links.add(company_link)

    def parse_company(self, response):
        # check response
        if response.status != 200:
            print(f"Failed to retrieve content. Status code: {response.status}")
            raise CloseSpider("Failed to retrieve content")
        # get company name
        company_name = response.css('h1.QuoteStrip-quoteTitle span.QuoteStrip-name::text').get()
        # navigate to url
        company_link = response.url
        self.driver.get(company_link)
        try:
            # check if the "More" button exists
            more_button = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//button[text()='More']"))
            )
            # scroll down to more button and click
            actions = ActionChains(self.driver)
            actions.move_to_element(more_button).perform()
            more_button.click()
            # wait for description to load
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.CompanyProfile-summary span"))
            )
            # get company description
            company_description = self.driver.find_element(By.CSS_SELECTOR, "div.CompanyProfile-summary span").text
            company_description = company_description.strip()
            yield {
                'link': company_link,
                'name': company_name,
                'description': company_description
            }
        except TimeoutException:
            try:
                company_description = self.driver.find_element(By.CSS_SELECTOR, "div.CompanyProfile-summary span").text
                company_description = company_description.strip()
                yield {
                    'link': company_link,
                    'name': company_name,
                    'description': company_description
                }
            except NoSuchElementException:
                print("Description element not found.")

    def closed(self, reason):
        self.driver.quit()  
    