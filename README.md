# ** Generic Ads.Txt Crawler **

A Python Scrapy Project which crawls the specified domains **ads.txt files** and retrieves the data in separate text files.

# Scrapy

Scrapy is a web scraping tool for python. You can install scrapy as a package in Python. Required version of python is *2.7 or higher*.

Use `pip install scrapy` to install the package or `python -m pip install --upgrade scrapy`

>In Linux, make sure you have root access for the code to use the ports.

# Running the spider

Use the command `scrapy runspider <file_name>` to start the spider. The spider will crawl the pages and store the content in the ads.txt files into separate text files. The generated text files will have the same name as the mentioned domains.

# Adding domains to domains.txt

Enter the domains that you need the spider to crawl inside this file. Enter the domains in the format '<domain-name><(.com/.net/.org)>'

