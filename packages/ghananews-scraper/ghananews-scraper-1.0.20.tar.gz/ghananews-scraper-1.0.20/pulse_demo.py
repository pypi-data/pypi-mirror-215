import requests
from bs4 import BeautifulSoup
from itertools import chain

url = f"https://www.ghanaiantimes.com.gh/"
# url = "https://www.ghanaiantimes.com.gh/category/politics/page/320/"
# url = "https://www.ghanaiantimes.com.gh/page/999/"
# https://www.ghanaiantimes.com.gh/category/business/page/401/
# https://www.ghanaiantimes.com.gh/category/local-sports/page/780/
# https://www.ghanaiantimes.com.gh/category/crime/page/292/
# https://www.ghanaiantimes.com.gh/category/tie-world/news-accross-africa/page/179/
# https://www.ghanaiantimes.com.gh/category/education/page/95/

# Send a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object with the response text and specify the parser
soup = BeautifulSoup(response.content, "html.parser")

links1 = soup.find_all("h2", class_="thumb-title")
links2 = soup.find_all("h2", class_="post-title")
pagination = soup.find("a", class_="block-pagination next-posts show-more-button")

page_urls1 = [link.a['href'] for link in links1]
page_urls2 = [link.a['href'] for link in links2]

pages_final = list(set(chain(page_urls1, page_urls2)))

for page in pages_final:
    data = requests.get(page)
    response_page = BeautifulSoup(data.content, 'html.parser')

    title = response_page.find("h1", class_="post-title entry-title").text.strip()
    published_date = response_page.find("span", class_="date meta-item tie-icon").text.strip()
    # category = response_page.find("span", class_="post-cat-wrap").find("a", class_="post-cat tie-cat-27").text.strip()
    content = response_page.find("div", class_="entry-content entry clearfix").find_all("p")
    all_text = ''.join(paragraph.get_text().strip().replace("Related Articles", "") for paragraph in content)

    print(all_text)
    print(published_date)
    # print(category)
    print(title)
    print("------------------")
    break

if __name__ == '__main__':
    pass
