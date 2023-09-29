from selenium import webdriver
from selenium.webdriver.common.by import By

# Set up the Selenium WebDriver
driver = webdriver.Chrome()

# Navigate to the URL
driver.get("https://www.cnbc.com/2023/07/07/stocks-making-the-biggest-premarket-moves-.html")

# Wait for the page to fully load
driver.implicitly_wait(15)

# Locate and click the "Reject All" button to close the cookie consent banner
reject_all_button = driver.find_element(By.ID, "onetrust-reject-all-handler")
reject_all_button.click()

print("Rejected cookies")

# Now locate and click the "Add to Watchlist" button
watchlist_button = driver.find_element(By.CSS_SELECTOR, ".AddToWatchlistButton-watchlistButton")
watchlist_button.click()

print("Added to watchlist")

driver.implicitly_wait(10)

# It's a good practice to close the driver once done
driver.quit()
