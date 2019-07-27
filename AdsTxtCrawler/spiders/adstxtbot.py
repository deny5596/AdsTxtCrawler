import scrapy
import scrapy.http.response
import win32api


class AdsTxtSpider(scrapy.Spider):
    name = "myspider"
    allowed_domains = []
    start_urls = []
    scraped_info = {}
    i = 0

    def __init__(self):
        for line in open('./domains.txt', 'r').readlines():
            self.allowed_domains.append(line.rstrip())
            self.start_urls.append(
                'http://{}/ads.txt'.format(line.rstrip()))

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print("Processing --> "+response.url)
        line = response.selector.xpath('//*/text()').getall()
        with open('{}.txt'.format(self.allowed_domains[self.i]), 'w', newline='\n', encoding='utf-8') as file:
            print("Writing ads.txt content into a file: %s" %
                  '{}.txt'.format(self.allowed_domains[self.i]))
            for content in line:
                file.write(content.rstrip("\r\n"))
            print('{} Completed'.format(self.allowed_domains[self.i]))
            file.close()
            self.i = self.i+1
