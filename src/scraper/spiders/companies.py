import scrapy
from scrapy.exceptions import CloseSpider
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import logging

class CompaniesSpider(scrapy.Spider):
    """
    Scrapes company information from CNBC.

    Attributes:
        name: The name of the spider.
        unique_links: A set of unique company links.
        driver: The Selenium webdriver.
        database: The database to store the scraped data. This is passed in from the caller.

    Methods:
        start_requests: Creates a request to the CNBC company list.
        parse: Parses the company list page.
        parse_links: Parses the company links from the company list page.
        parse_company: Parses the company information from the company page.
        closed: Closes the Selenium webdriver.
    """
    def __init__(self):
        # Initialize the spider
        self.name = "companies"
        self.unique_links = set()
        self.driver = webdriver.Chrome()
        self.WAIT_TIME = 15

    def start_requests(self):
        # Cnbc company list entrypoint
        yield scrapy.Request(url="https://www.cnbc.com/nasdaq-100/", callback=self.parse)

    def parse(self, response):
        try:
            if response.status != 200:
                logging.error(f"Failed to retrieve content. Status code: {response.status}")
                raise CloseSpider("Failed to retrieve content")

            self.driver = webdriver.Chrome()
            self.driver.get(response.url)

            self.parse_links()
            self.accept_cookies()

            for url in self.unique_links:
                yield scrapy.Request(url, callback=self.parse_company)
        except Exception as e:
            logging.error(f"Failed to parse company list: {e}")

    def accept_cookies(self):
        try:
            accept_cookies_button = WebDriverWait(self.driver, self.WAIT_TIME).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            accept_cookies_button.click()
        except TimeoutException:
            logging.warning("Cookies accept button not found, continuing without accepting.")

    def parse_links(self):
        # Wait for links to load
        WebDriverWait(self.driver, self.WAIT_TIME).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href^="//www.cnbc.com/quotes/"]'))
        )
        company_links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href^="//www.cnbc.com/quotes/"]')
        
        # Store unique links
        for link in company_links:
            company_link = link.get_attribute("href")
            self.unique_links.add(company_link)

    def parse_company(self, response):
        try:
            if response.status != 200:
                logging.error(f"Failed to retrieve content. Status code: {response.status}")
                raise CloseSpider("Failed to retrieve content")

            company_name = response.css('h1.QuoteStrip-quoteTitle span.QuoteStrip-name::text').get()
            company_link = response.url

            self.driver.get(company_link)

            try:
                more_button = WebDriverWait(self.driver, self.WAIT_TIME).until(
                    EC.presence_of_element_located((By.XPATH, "//button[text()='More']"))
                )
                actions = ActionChains(self.driver)
                actions.move_to_element(more_button).perform()
                more_button.click()

                WebDriverWait(self.driver, self.WAIT_TIME).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.CompanyProfile-summary span"))
                )

                company_description = self.driver.find_element(By.CSS_SELECTOR, "div.CompanyProfile-summary span").text
                company_description = company_description.strip()

                yield {
                    'link': company_link,
                    'name': company_name,
                    'description': company_description
                }
            except TimeoutException:
                company_description = self.driver.find_element(By.CSS_SELECTOR, "div.CompanyProfile-summary span").text
                company_description = company_description.strip()

                yield {
                    'link': company_link,
                    'name': company_name,
                    'description': company_description
                }
            except NoSuchElementException:
                logging.warning("Description element not found.")
        except Exception as e:
            logging.error(f"Error in parse_company: {e}")

    def closed(self, reason):
        """
        Closes the Selenium webdriver.
        """
        try:
            if self.driver:
                self.driver.quit()
        except Exception as e:
            logging.error(f"Error while cleaning up webdriver: {e}")
    