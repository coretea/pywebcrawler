from bs4 import BeautifulSoup
from requests import urllib3, Request
import pymongo
import sys
import json



# --------- Classes-------
class FirmwareFile:
    'this class represents the firmware Files extracted from the site'
    # initializer for an instance of firmware file
    def __init__(self, brand, model, name, stock_custom, android_v, author, download_URL):
        self.brand = brand
        self.model = model
        self.name = name
        self.stock_custom = stock_custom
        self.android_v = android_v
        self.author = author
        self.download_URL = download_URL


class Scraper:
    'This class used for scraping the HTML code for items and parse them'
    #-----------vars-----------
    url = sys.argv[1] + "/firmware-downloads" # first page of firmware files. gets the main url from console argument
        # http url manager
    http = urllib3.PoolManager()
    #----------functions------
    def parser(self):
        """
        this function parsing the entire website using multiple functions
        function returns the output of the parsing to items.
        (text only)
        """
        print("Starting Scan...\nThis might take a minute")
        isDone = False
        output = []
        #while you can still go next in pages
        while not isDone:
            #getting the html page
            page_html = self.http.request('GET', self.url)
            # HTML parsing
            page_soup = BeautifulSoup(page_html.data, "html.parser")
            # get table element from the soup
            table = page_soup.find("table")
            output_rows = []
            # parse the table into the list of the output.
            for table_row in table.findAll('tr'):
                columns = table_row.findAll('td')
                output_row = []
                fileurl = ""
                for column in columns:
                    output_row.append(column.text)
                    # gets the file url
                    file1 = column.find("a", href=True)
                    if file1 is not None:
                        fileurl = file1['href']
                        fileurl = fileurl.replace('\\','/') # switches the backslah to slash for url
                        output_row.append(self.get_download_url(fileurl)) # gets file download url for each file

                output_rows.append(output_row)
            output_rows.remove(output_rows[0])# first element is empty
            output.extend(output_rows)
            # gets the next page. if there isnt one, return True
            isDone = self.get_next_page(page_soup)
        print("Scan Complete!")
        return output

    def get_next_page(self, page_soup):
        """
        this function gets the page soup (scraped html)
        and searches for the next page url
        """
        next = page_soup.find("a", {"title":"Go to next page"})
        if (next == None):
            return True
        self.url = sys.argv[1] + "/"+ next['href']
        return False

    def create_items(self, output_list):
        """
        function gets the output list and created instances of FirmwareFile
        """
        files_list = []
        for filestr in output_list:
            # the strip function helps to keep the text simple without any unicode adding spaces and tabs
            files_list.append(FirmwareFile(filestr[0].strip(' \t\n\r'),
             filestr[1].strip(' \t\n\r'),
             filestr[2].strip(' \t\n\r'),
             filestr[6].strip(' \t\n\r'),
             filestr[4].strip(' \t\n\r'),
             filestr[5].strip(' \t\n\r'),
             filestr[3].strip(' \t\n\r')))

        return files_list


    def get_download_url(self, url):
        """
        this function gets a url ending to the file and searches for download file links
        """
        fileurl = sys.argv[1] + "/"+ url
        page_html = self.http.request('GET', fileurl)
        soup = BeautifulSoup(page_html.data, "html.parser")
        allhrefs = soup.findAll("a", href=True)
        downloadurl = "none"
        for href in allhrefs:
            if "http://www.rockchipfirmware.com/sites/default/files/" in href['href']:
                downloadurl = href['href']
        return downloadurl


class db_access:
    'A class for database access functions and variables'
    client = pymongo.MongoClient('localhost', 27017)
    mydb = client["db_data"]
    metadata_collection = mydb["metadata"]

    def itemsToDicts(self, items_list):
        """
        mongoDB works with dicts, this function casts item list to dicts list
        """
        for i in range(0, len(items_list)):
            items_list[i] = items_list[i].__dict__


    def upload_items(self, items_list):
        """
        function checks if item exists in db and of not, will upload item
        """
        print("Uploading Items to DB at localhost:27017")
        for item in items_list:
            if not self.does_exist(item):
                self.metadata_collection.insert_one(item)
        print("Upload Complete!")


    def does_exist(self, item_dict):
        """
        this function gets item dict and checks if item exists in DB
        """
        if self.metadata_collection.count_documents(item_dict, limit = 1) != 0:
            return True
        return False




#testing
scraper = Scraper()
db = db_access()
output = scraper.parser()
files = scraper.create_items(output)
db.itemsToDicts(files)
db.upload_items(files)
