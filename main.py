import requests
from bs4 import BeautifulSoup

# Specify the URL of the website you want to scrape
url = "https://www.cnbc.com/finance/"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Initialize a set to store unique links
    unique_links = set()

    # Find and extract links to articles (adjust the HTML structure based on the specific website)
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        if href.startswith("https://www.cnbc.com/20"):
            unique_links.add(href)

    # Print the unique links to articles
    for link in unique_links:
        print(link)
else:
    print(f"Failed to retrieve content. Status code: {response.status_code}")
