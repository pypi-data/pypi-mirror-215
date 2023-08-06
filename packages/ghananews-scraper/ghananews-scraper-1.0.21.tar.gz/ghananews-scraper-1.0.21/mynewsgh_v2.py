import requests
from bs4 import BeautifulSoup

url = "https://www.mynewsgh.com/category/politics/"

# Create a session object to reuse the underlying TCP connection
session = requests.Session()

response_page = session.get(url)
soup = BeautifulSoup(response_page.text, "html.parser")
pages = soup.find_all("li", class_="mvp-blog-story-wrap left relative infinite-post")

last_page = soup.find("div", class_="pagination").span.text.split(" ")[-1]
page_url_list = [url + f"page/{page}/" for page in range(1, int(last_page) + 1)]

for page_url in page_url_list:
    response_page = session.get(page_url)
    soup = BeautifulSoup(response_page.text, "html.parser")
    pages = soup.find_all("li", class_="mvp-blog-story-wrap left relative infinite-post")

    articles = [page.a['href'] for page in pages]

    for url in articles:
        response_page = session.get(url)
        soup_page = BeautifulSoup(response_page.text, "html.parser")

        title = soup_page.find("h1", class_="mvp-post-title left entry-title").text.strip()
        published_date = soup_page.find("time", class_="post-date updated").text.strip()
        author = soup_page.find("span", class_="author-name vcard fn author").find("a").text.strip()
        content = [content.text.strip() for content in soup_page.find("div", {"id": "mvp-content-main"}).find_all("p")]

        print(title)
        print(published_date)
        print(author)
        print(' '.join(content))
        print("------------------")

if __name__ == '__main__':
    session.close()

