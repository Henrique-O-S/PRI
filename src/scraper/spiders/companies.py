import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CompaniesSpider(scrapy.Spider):
    name = "companies"

    def __init__(self):
        self.driver = webdriver.Chrome()

    def parse(self, response):
        company_name = response.css('h1.QuoteStrip-quoteTitle span.QuoteStrip-name::text').get()
        company_stock_price = response.css('div.QuoteStrip-lastPriceStripContainer span.QuoteStrip-lastPrice::text').get()

        if company_name:
            print(f"Company Name: {company_name}")
        if company_stock_price:
            print(f"Company Stock Price: {company_stock_price}")

        more_button = self.driver.find_element(By.XPATH, '//button[text()="More"]')
        if more_button:
            more_button.click()

            expanded_text_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.CompanyProfile-descriptionContainer span'))
            )

            expanded_text = expanded_text_element.text.strip()
            if expanded_text:
                print(f"Complete Description: {expanded_text}")

    def closed(self, reason):
        self.driver.quit()  
