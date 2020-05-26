# pywebcrawler


# Python Web Crawler Program - ArcusTeam

NOTE: This Web Crawler works only with this specific site: "www.rockchipfirmware.com"
This Web Crawler allows you to scan Firmware Files from ROCKCHIP FIRMWARE and upload their metadata to a MongoDB Database
right in your localhost.

Another main feature is downloading Firmware files to your device straight from your local DB.

### Prerequisites

This software is made to work with Ubuntu 18.04.X and up, Python 3.6 and up.


###  Usagwe

This software runs from the shell command line on your Ubuntu machine.
The usage should look like that:

```
python3 main.py [OPTIONS] [URL]

```

arguments for options:

```
-s for scanning and updating DB
-d for downloading a certain file from DB.
```


## Authors

* **Omer Kvartler**
