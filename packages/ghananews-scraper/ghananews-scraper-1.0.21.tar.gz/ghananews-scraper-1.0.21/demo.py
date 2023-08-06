from bs4 import BeautifulSoup
import requests
import csv
import asyncio
import aiohttp

search_query = "laptops"
page = 1

BASE_URL = "https://tonaton.com"

# query = https://tonaton.com/search?region=ashanti&query=houses&page=1
# query = https://tonaton.com/c_vehicles?region=ashanti&page=1
# query = https://tonaton.com/r_ashanti/c_real-estate?page=2

tonaton = f"https://tonaton.com/search?query={search_query}&page={page}"
data = requests.get(url=tonaton).content
soup = BeautifulSoup(data, 'html.parser')
page_numbers = soup.find("section", class_="pagination")
total_pages = int(page_numbers.text.strip().replace("\n", ",").split(",")[-2])


async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def main():
    with open(f"{search_query}_data.csv", "w", newline="") as csv_file:
        fieldnames = ["product_description", "price", "location", "photo", "page_url"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for page in range(1, total_pages + 1):
            tonaton_url = f"https://tonaton.com/search?query={search_query}?page={page}"

            task = asyncio.create_task(fetch_data(tonaton_url))
            results = await task

            html_soup = BeautifulSoup(results, 'html.parser')

            items = html_soup.find_all('a', class_='product__item')

            for item in items:
                product_description = item.find('p', class_='product__description').get_text(strip=True)

                location = item.find('p', class_='product__location').get_text(strip=True)

                price = item.find('span', class_='product__title').get_text(strip=True)

                # size_tags = item.find('div', class_='product__tags').find_all('span')
                # size = [tag.get_text(strip=True) for tag in size_tags if 'sqm' in tag.get_text(strip=True).lower()][0]

                link = BASE_URL + item['href']

                photos = item.find("div", class_="product__image").find_all("img", class_="h-opacity-0_8")
                photo = [photo['src'] for photo in photos][0]

                # soup_response = requests.get(url=link).text
                # soup_page = BeautifulSoup(soup_response, 'html.parser')
                # contact = soup_page.find("div", class_="details__contact flex wrap").find("a", class_="b-show-contact h-mr-5")
                # print(contact)

                writer.writerow({
                    "product_description": product_description,
                    "price": str(price).split(" ")[-1],
                    "location": location,
                    "photo": photo,
                    "page_url": link
                })

            print("Page " + str(page) + " scraped successfully!")
    print("Scrape complete!!!")


#
# with open("yen_data.csv", "w", newline="") as csv_file:
#     fieldnames = ["title", "content", "published_date", "author", "page_url"]
#     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#     writer.writeheader()
#
#     for url in links:
#         soup_response = requests.get(url=url).text
#         soup_page = BeautifulSoup(soup_response, 'html.parser')
#
#         title = soup_page.find("h1", class_="c-main-headline")
#         title_main = title.text.strip()
#
#         content_main = ""
#         content_div = [item for item in soup_page.find("div", {"class": "post__content"}).select("ul li strong")]
#
#         for tag in content_div:
#             content_main = content_main + tag.get_text().strip() if tag else ""
#
#         meta_date = soup_page.find("div", {"class": "c-article-info post__info"})
#         published_date = meta_date.text.strip() if meta_date else ""
#
#         author = soup_page.find("a", {"class": "c-article-info__author"}).text.strip()
#
#         writer.writerow(
#             {"title": title_main,
#              "content": content_main,
#              "published_date": published_date,
#              "author": author,
#              "page_url": url}
#         )

if __name__ == '__main__':
    asyncio.run(main())
