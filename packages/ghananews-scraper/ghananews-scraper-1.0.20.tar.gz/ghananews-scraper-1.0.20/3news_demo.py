# import requests
# from bs4 import BeautifulSoup
# import csv
#
# url = "https://3news.com/category/news/"
# payload = {'page': 1}
#
# num_pages_to_load = 50
# pages_loaded = 1
#
# session = requests.Session()
#
# with open("threenews.csv", mode="w", newline="", encoding='utf-8') as csv_file:
#     fieldnames = ["title", "content", "author", "published_date", "page_url"]
#     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#     writer.writeheader()
#
#     try:
#         while pages_loaded < num_pages_to_load:
#             try:
#                 response = session.get(url, params=payload)
#                 response.raise_for_status()
#                 payload['page'] += 1
#
#                 next_soup = BeautifulSoup(response.content, 'html.parser')
#                 pages = next_soup.find_all("h3", class_="entry-title td-module-title")
#
#                 PAGE_LIST = [page.a['href'] for page in pages]
#                 print(PAGE_LIST)
#
#                 pages_loaded += 1
#
#             except requests.exceptions.RequestException as e:
#                 print("Error occurred during page retrieval:", e)
#
#         rows = []
#         for page_url in PAGE_LIST:
#             try:
#                 response_page = session.get(page_url)
#                 response_page.raise_for_status()
#
#                 soup = BeautifulSoup(response_page.text, "html.parser")
#
#                 title = soup.find("h1", class_="entry-title").text.strip()
#                 published_date = soup.find("time", class_="entry-date updated td-module-date").text.strip()
#                 author = soup.find("div", class_="td-post-author-name").find("a").text.strip()
#                 content = [content.text.strip() for content in soup.find("div", class_="td-post-content tagdiv-type").find_all("p")]
#
#                 rows.append({
#                     "title": title,
#                     "content": ' '.join(content),
#                     "author": author,
#                     "published_date": published_date,
#                     "page_url": page_url
#                 })
#
#             except requests.exceptions.RequestException as e:
#                 print("Error occurred during page retrieval:", e)
#             except AttributeError:
#                 print("Attribute not found on page:", page_url)
#
#         writer.writerows(rows)
#
#     except Exception as e:
#         print("Error occurred:", e)
#
# if __name__ == '__main__':
#     print("Scraping complete.")










import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os


url = "https://3news.com/category/news/"
# Example using AJAX request to load more content
payload = {'page': 1}  # Modify the payload according to the AJAX request parameters

# Iterate to load more pages until you reach the desired number of pages or a specific condition
num_pages_to_load = 100
pages_loaded = 1

with open(
        "threenews.csv",
        mode="w",
        newline="",
        encoding='utf-8'
) as csv_file:
    fieldnames = ["title", "content", "author", "published_date", "page_url"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    PAGE_LIST = []
    while pages_loaded < num_pages_to_load:
        # Send the AJAX request to load more content
        response = requests.get(url, params=payload)
        payload['page'] += 1  # Update the payload for the next request

        # Create a BeautifulSoup object from the response content
        next_soup = BeautifulSoup(response.content, 'html.parser')

        # Process the content of the newly loaded page
        # ... (add your code here to extract the desired data)
        pages = next_soup.find_all("h3", class_="entry-title td-module-title")

        # page_list = [page.a['href'] for page in pages]
        for page in pages:
            PAGE_LIST.append(page.a['href'])

        # Increment the counter
        pages_loaded += 1

    for url in PAGE_LIST:
        response_page = requests.get(url)
        soup = BeautifulSoup(response_page.text, "html.parser")

        title = soup.find("h1", class_="entry-title").text.strip()
        published_date = soup.find("time", class_="entry-date updated td-module-date").text.strip()
        author = soup.find("div", class_="td-post-author-name").find("a").text.strip()
        content = [content.text.strip() for content in soup.find("div", class_="td-post-content tagdiv-type").find_all("p")]

        # print(title)
        # print(published_date)
        # print(''.join(content))
        # print(author)
        # print("--------------------------")
        writer.writerow(
            {
                "title": title,
                "content": ' '.join(content),
                "author": author,
                "published_date": published_date,
                "page_url": url
            }
        )

if __name__ == '__main__':
    pass

