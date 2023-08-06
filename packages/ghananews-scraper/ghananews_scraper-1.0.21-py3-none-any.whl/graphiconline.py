from bs4 import BeautifulSoup
import requests
import csv

BASE_PAGE = 'https://www.graphic.com.gh'
graphic = "https://www.graphic.com.gh/international.html"

data = requests.get(url=graphic).text

soup = BeautifulSoup(data, 'html.parser')
pages = soup.find_all('td', class_='list-title')

url_lst = []
for page in pages:
    urls = BASE_PAGE + page.a['href']
    url_lst.append(urls)
    # title = page.a.text

with open("graphic_data.csv", "w", newline="") as csv_file:
    fieldnames = ["title", "content", "published_date", "page_url"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for url in url_lst:
        soup_response = requests.get(url=url).text
        soup_page = BeautifulSoup(soup_response, 'html.parser')

        title = soup_page.find("div", class_="article-header")
        title_main = title.text.strip()

        content_main = None
        content = soup_page.find("div", {"class": "article-details"}).select("div p")
        for tag in content:
            content_main = tag.get_text().strip() if tag else ""
        # content_main = str(content).strip()

        meta_date = soup_page.find("div", {"class": "article-info"}).find("span", class_="published")
        published_date = meta_date.text.strip()

        writer.writerow(
            {"title": title_main, "content": content_main, "published_date": published_date, "page_url": url}
        )

if __name__ == '__main__':
    pass
