from urllib.parse import urljoin

import scrapy
import scrapy.crawler
import scrapy.http.request
import scrapy.http.response
from scrapy.crawler import CrawlerProcess


class AdsTxtSpider(scrapy.Spider):
    name = "myspider"
    allowed_domains = []
    start_urls = []
    scraped_info = {}
    # Handing HTTP Status Codes like redirects, not found, etc
    handle_httpstatus_list = [400, 401, 403, 404, 410, 500, 502, 503, 504, 522]
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html, application/xhtml+xml, application/xml; q = 0.9, image/webp, image/apng, */*; q = 0.8, application/signed-exchange; v = b3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache'}
    }

    def __init__(self):
        # Reading domains from an external text file
        for line in open('./domains.txt', 'r').readlines():
            self.allowed_domains.append(line)
            self.start_urls.append(
                urljoin('http://{}'.format(line.rstrip()), 'ads.txt'))

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print("Processing --> "+response.url)
        responseMetaInfo = response.request.meta if response.request.meta else None

        # Scraping data from the page using Xpath to avoid irrelevant data
        data = response.xpath(
            '//*[not(ancestor-or-self::script or descendant-or-self::script or ancestor-or-self::noscript or descendant-or-self::noscript or ancestor-or-self::style or descendant-or-self::style)]/text()').getall()
        seller_relation = ''
        adstxtstatus = 0
        track = 0

        # Storing appropriate HTTP Status Codes
        if response.status == 200:
            httpstatus = response.status
            adstxtstatus = 1
        else:
            if 'redirect_reasons' in responseMetaInfo:
                httpstatus = responseMetaInfo['redirect_reasons'][len(
                    responseMetaInfo['redirect_reasons'])-1]
                adstxtstatus = 2
            else:
                httpstatus = response.status
                adstxtstatus = 3

        # Retrieving original URL if there's a redirect
        if responseMetaInfo.get('redirect_urls'):
            url = responseMetaInfo['redirect_urls'][0]
        else:
            url = response.request.url

        # Writing scraped Data into a text file
        with open('Temp.txt', 'w', newline='\n', encoding='utf-8') as tempFile:
            for entry in data:
                tempFile.write(entry.rstrip("\r\n"))
            tempFile.close()

        # Reading the temporarily stored Data
        file = open('Temp.txt', 'r')

        # Storing ads.txt entries in dict (scraped_info) to be written in the final CSV output
        for row in file:
            seller_relation = "Direct" if "direct" in str.lower(
                row) else "Reseller"

            if "direct" in str.lower(row) or "reseller" in str.lower(row):
                track = 1
                self.scraped_info = {
                    'Domain Name': (url.replace('http://', '')).replace('/ads.txt', ''),
                    'Ads.txt': adstxtstatus,
                    'Ads.txt Line': row.rstrip("\n"),
                    'Seller Relation': seller_relation,
                    'HTTP Status Code': httpstatus,
                }
                yield self.scraped_info
        if track == 0:
            self.scraped_info = {
                'Domain Name': (url.replace('http://', '')).replace('/ads.txt', ''),
                'Ads.txt': adstxtstatus,
                'Ads.txt Line': row.rstrip("\n"),
                'Seller Relation': seller_relation,
                'HTTPStatusCode': httpstatus,
            }
            yield self.scraped_info
