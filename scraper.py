from bs4 import BeautifulSoup
from requests import urllib3, Request
import pymongo
import sys

class Scraper:
    'This class used for scraping the HTML code for items and parse them'
    pass

# http url manager
http = urllib3.PoolManager()
# url for scraping the items
url = "https://www.rockchipfirmware.com/firmware-downloads"
#getting the html page
page_html = http.request('GET', url)
# HTML parsing
page_soup = BeautifulSoup(page_html.data, "html.parser")
# get table element from the soup
table = page_soup.find("table")

output_rows = []
# parse the table into the list of the output
for table_row in table.findAll('tr'):
    columns = table_row.findAll('td')
    output_row = []
    for column in columns:
        output_row.append(column.text)
    output_rows.append(output_row)

print(output_rows)
