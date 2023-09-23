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

    # Find and extract links from <a> elements inside <div> elements with only one child
    for div_tag in soup.find_all('div'):
        # Check if the div_tag has only one child and that child is an <a> element
        if len(div_tag.find_all()) == 1 and div_tag.find('a'):
            # Get the href attribute of the child <a> element
            href = div_tag.find('a').get('href')
            if href and href.startswith("https://www.cnbc.com/20"):
                unique_links.add(href)

    # Print the valid links
    for link in unique_links:
        print(link)
else:
    print(f"Failed to retrieve content. Status code: {response.status_code}")
