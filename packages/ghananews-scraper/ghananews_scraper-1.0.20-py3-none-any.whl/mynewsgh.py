import requests
from bs4 import BeautifulSoup

url = "https://www.mynewsgh.com/category/politics/"

response_page = requests.get(url)
soup = BeautifulSoup(response_page.text, "html.parser")
pages = soup.find_all("li", class_="mvp-blog-story-wrap left relative infinite-post")

page_num = soup.find("div", class_="pagination")
last_page = page_num.span.text.split(" ")[-1]

page_url_list = [url + f"page/{page}/" for page in range(1, int(last_page) + 1)]
print(page_url_list)
# for page in range(1, int(last_page) + 1):
#     urls = url + f"page/{str(page)}/"
#     page_url_list.append(urls)


next_page_urls = []
for page_url in page_url_list[:10]:
    response_page = requests.get(page_url)
    soup = BeautifulSoup(response_page.text, "html.parser")
    pages = soup.find_all("li", class_="mvp-blog-story-wrap left relative infinite-post")

    for page in pages:
        url = page.a['href']
        next_page_urls.append(url)

for url in next_page_urls:
    with requests.Session() as session:
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
    #break

if __name__ == '__main__':
    pass
