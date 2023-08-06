import re
import urllib.parse
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

# URL of the job site
url = "https://www.civilservicejobs.service.gov.uk/csr/index.cgi?SID=cGFnZWNsYXNzPVNlYXJjaCZvd25lcnR5cGU9ZmFpciZwYWdlYWN0aW9uPXNlYXJjaGNvbnRleHQmc29ydD1zY29yZSZwYWdlPTEmY29udGV4dGlkPTIzNTU3NDM1Jm93bmVyPTUwNzAwMDAmcmVxc2lnPTE2NzQ4Nzk5NTMtMzA4ODNhODBkZDVhZjE2YjAzN2MwYWU0ZWZmN2MxNjI0ZTM5NDZmZQ=="

# Create a webdriver to control the browser
driver = webdriver.Firefox()

# Navigate to the job site
driver.get(url)

# Parse the HTML content
soup = BeautifulSoup(driver.page_source, "html.parser")

# next_page_link = soup.find("a", {"class": "search-results-paging-menu"})
# if next_page_link:
#     url = next_page_link["href"]
#     print(url)
# else:
#     print("Last Page")

# Find all the job listings on the page
job_listings = soup.find_all("div", class_="search-results-job-box-title")

ids = []
# Loop through each job listing
for job in job_listings:
    # Find the job link
    job_link = job.find("a")
    # Click on the link to open the job
    driver.get(job_link["href"])
    # Parse the HTML content of the job page
    job_soup = BeautifulSoup(driver.page_source, "html.parser")
    # Find the "Share" button
    share_button = job_soup.find("a", class_="email")

    # Extract the job code from the button's href attribute
    job_code = share_button["href"]

    # extract body from the mailto:
    parsed_url = urllib.parse.urlsplit(job_code)
    query_string = parsed_url.query
    body = urllib.parse.parse_qs(query_string)["body"][0]

    # extract jobcode from mailto:
    job_id = re.search(r"jcode=(\d+)", body).group(1)
    # Print the job code/id
    print(f"Job Code is: {job_id}")

    # add these job_ids to the list
    ids.append(job_id)

if __name__ == "__main__":

    df = pd.DataFrame()
    df["jobcodes"] = pd.Series(ids).values
    df.to_csv("jobcodes.csv")

    # Close the browser
    driver.quit()
