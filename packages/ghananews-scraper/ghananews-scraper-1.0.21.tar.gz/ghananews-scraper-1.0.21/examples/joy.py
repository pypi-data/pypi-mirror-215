# Option 1.
from myjoyonline.scraper import MyJoyOnline

if __name__ == '__main__':
    url = 'https://myjoyonline.com/politics'
    print(f"Downloading data from: {url}")
    joy = MyJoyOnline(url=url)
    joy.download()
