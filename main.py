from webcrawler_modules import Scraper, db_access, FirmwareFile
import sys

HELP_MSG = "USAGE: \"python3 main.py [OPTIONS] [URL]\"\nOPTIONS:\n-s for scanning and updating DB\n-d for downloading a certain file from DB."


def check_arguments():
    """
    this function checks the validality of arguments inserted when running main.pys
    """
    if len(sys.argv) != 3:
        print("Invalid Arguments.\n")
        print(HELP_MSG)
        exit()

    if (sys.argv[1] != "-s" and sys.argv[1] != "-d"):
        print("Invalid option\n")
        print(HELP_MSG)
        exit()

    if(sys.argv[2] != "www.rockchipfirmware.com"):
        print("Sorry, this website is not supported")
        exit()

# global variables
check_arguments()
scraper = Scraper()
db = db_access()


def download_option():
    """
    this function is for the download file option.
    dialog with user asking for brand, model and file for download.
    checking input for each step. (while for each step)
    """
    flag = True
    while(flag):
        flag2 = True
        while(flag2):
            brand = input("\nEnter brand name(Case-Sensitive): ")
            models = db.get_models(brand)
            if models == None:
                continue
            break

        while(flag2):
            print("Choose a model: ")
            for item in models:
                print(str(models.index(item))+") "+item)
            model_choice = input("\nChoose a model(by number): ")
            if int(model_choice) > len(models) or  int(model_choice) < 0:
                print("Invalid choice.")
                continue
            break

        while(flag2):
            names = db.get_names(models[int(model_choice)])
            if names == None:
                continue
            break

        while(flag2):
            print("Choose a file: ")
            for item in names:
                print(str(names.index(item))+") "+item)
            file_choice = input("\nChoose a file(by number): ")
            if int(file_choice) > len(names) or  int(file_choice) < 0:
                print("Invalid choice.")
                continue
            break


        downloadurl = db.get_download_by_name(names[int(file_choice)])
        if downloadurl == "none":
            print("There is no download available for this file. Sorry :(")
            exit()

        print("Download Started!")
        scraper.download_file(downloadurl)



def main():
    if sys.argv[1] == "-s":
        # if the user chose scan option
        output = scraper.parser() # scanning site
        files = scraper.create_items(output) # creating items
        db.itemsToDicts(files) # casting items to dicts for uploading
        db.upload_items(files) # uploading items to db

    # if user chose downloading options
    if sys.argv[1] == "-d":
        download_option()


if __name__ == "__main__":
    main()
