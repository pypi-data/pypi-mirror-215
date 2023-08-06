import requests
from bs4 import BeautifulSoup
import csv
import os

author = "laud-nartey"

url = f"https://3news.com/author/laud-nartey/"
data = requests.get(url)
soup = BeautifulSoup(data.content, "html.parser")

last_page = int(soup.find("a", class_="last").text.strip().replace(",", ""))

for page_num in range(1, last_page + 1):
    url_link = f"https://3news.com/author/{author}/page/{page_num}/"
    data = requests.get(url_link)
    soup_page = BeautifulSoup(data.content, "html.parser")

    # for each page number find all urls:
    urls = soup_page.find("h3", class_="entry-title td-module-title").find("a")['href']

    response_page = requests.get(urls)
    data_page = BeautifulSoup(response_page.text, 'html.parser')

    # find author
    author = data_page.find("div", class_="td-post-author-name").find("a").text.strip()
    # find published date
    published_date = data_page.find("time", class_="entry-date updated td-module-date").text.strip()
    # find entry category
    category = data_page.find("li", class_="entry-category").find("a").text.strip()
    # find title
    title = data_page.find("h1", class_="entry-title").text.strip()
    # find content
    content = [content.text.strip() for content in data_page.find("div", class_="td-post-content tagdiv-type").find_all("p")]
    # content = data_page.find("div", class_="td-post-content tagdiv-type").find_all("p")

    print(urls)
    print(title)
    print(category)
    print(author)
    print(published_date)
    print(''.join(content))
    print("----------------")

if __name__ == '__main__':
    print(last_page)
