from bs4 import BeautifulSoup
from requests import urllib3, Request
import pymongo
import sys
import json

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

    def json(self):
        pass

class Scraper:
    'This class used for scraping the HTML code for items and parse them'
    #-----------vars-----------
    url = sys.argv[1] + "/firmware-downloads" # first page of firmware files. gets the main url from console argument

    #----------functions------
    def parser(self):

        isDone = False
        # http url manager
        http = urllib3.PoolManager()
        output = []
        #while you can still go next in pages
        while not isDone:
            #getting the html page
            page_html = http.request('GET', self.url)
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

            output_rows.remove(output_rows[0])# first element is empty
            output.extend(output_rows)
            # gets the next page. if there isnt one, return True
            isDone = self.get_next_page(page_soup)
            
        return output

    def get_next_page(self, page_soup):
         next = page_soup.find("a", {"title":"Go to next page"})
         if (next == None):
             return True
         self.url = sys.argv[1] + "/"+ next['href']
         return False

    def create_items(self, output_list):
        files_list = []
        print(output_list)
        for filestr in output_list:
            # the strip function helps to keep the text simple without any unicode adding spaces and tabs
            files_list.append(FirmwareFile(filestr[0].strip(' \t\n\r'),
             filestr[1].strip(' \t\n\r'),
             filestr[2].strip(' \t\n\r'),
             filestr[3].strip(' \t\n\r'),
             filestr[4].strip(' \t\n\r'),
             filestr[5].strip(' \t\n\r')))
        return files_list



class db_access:
    'A class for database access functions and variables'
    client = pymongo.MongoClient('localhost', 27017)
    mydb = client["db_data"]
    metadata_collection = mydb["metadata"]


#testing
scraper = Scraper()
output = scraper.parser()
files = scraper.create_items(output)
print(len(files))
print(files[1].name)
