from bs4 import BeautifulSoup
from requests import urllib3, Request
import pymongo
import sys

# --------- Classes-------
class FirmwareFile:
    'this class represents the firmware Files extracted from the site'
    # initializer for an instance of firmware file
    def __init__(self, brand, model, name, stock_custom, android_v, author):
        self.brand = brand
        self.model = model
        self.name = name
        self.stock_custom = stock_custom
        self.android_v = android_v
        self.author = author

class Scraper:
    'This class used for scraping the HTML code for items and parse them'

    def parser(url):
        # http url manager
        http = urllib3.PoolManager()
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
        return output_rows

    def create_items(output_list):
        files_list = []
        for i in range(1, len(output_list)):
            files_list.append( FirmwareFile(output[i][0], output[i][1], output[i][2], output[i][3], output[i][4], output[i][5]))
        return files_list

class db_access:
    'A class for database access functions and variables'
    client = pymongo.MongoClient('localhost', 27017)
    mydb = client["db_data"]
    metadata_collection = mydb["metadata"]



# url for scraping the items
url = "https://www.rockchipfirmware.com/firmware-downloads"
output = Scraper.parser(url)
files = Scraper.create_items(output)
