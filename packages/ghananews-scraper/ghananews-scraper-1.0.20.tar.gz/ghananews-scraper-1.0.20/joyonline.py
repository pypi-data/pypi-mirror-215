import csv
import time
import unicodedata

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.options import Options

# Set up Selenium options
chrome_options = Options()
# Run Chrome in headless mode
chrome_options.add_argument("--headless")
chrome_options.page_load_timeout = 600  # 300 seconds
chrome_options.implicitly_wait = 600    # 300 seconds

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(options=chrome_options)

BASE = "https://myjoyonline.com"

# URL of the webpage to scrape
BASE_URL = "https://myjoyonline.com/politics"

# Open the webpage
driver.get(BASE_URL)

NUMBER_TIMES_TO_SCROLL = 5

for _ in range(NUMBER_TIMES_TO_SCROLL):
    # Perform scrolling actions to reveal hidden content
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait for some time to allow the page to load more content
    time.sleep(2)

# Parse the HTML content
soup = BeautifulSoup(driver.page_source, "html.parser")

# Find all the pages
pages = soup.find_all("div", class_="feeditem")

URLS = [BASE + page_link.find("a")['href'] for page_link in pages]

# for page in pages:
#     # Find the page link
#     page_link = page.find("a")
#     URLS.append(BASE + page_link['href'])

with open("joy_main.csv", "w", newline="") as csv_file:
    fieldnames = ["title", "content", "author", "published_date", "page_url"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for url in URLS:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        title = soup.find("div", class_="article-title")
        if title is not None:
            title = title.text.strip()
            title = unicodedata.normalize("NFKD", title).encode("ASCII", "ignore").decode("utf-8")
        else:
            print("article title element not found.")

        content = soup.find_all("div", class_="article-text")
        content = "\n".join([element.text.strip() for element in content])
        content = unicodedata.normalize("NFKD", content).encode("ASCII", "ignore").decode("utf-8")

        source = soup.find("div",
                           {
                               "style": "color: rgb(151, 146, 146); font-size: 12px; margin: 10px 0px; display: flex; justify-content: space-between;"})

        author = None
        published_date = None
        if source is not None:
            spans = source.find_all("span")
            if len(spans) == 2:
                author = spans[0].text.strip().split(":")[-1]
                published_date = spans[1].text.strip()
            else:
                print("Invalid number of <span> elements found.")
        else:
            print("No source element found")

        writer.writerow(
            {
                "title": title,
                "content": content,
                "author": author,
                "published_date": published_date,
                "page_url": url
            }
        )

if __name__ == '__main__':
    # Close the browser
    driver.quit()
