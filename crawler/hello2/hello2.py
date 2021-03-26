import scrapy

class BlogSpider(scrapy.Spider):
    name = 'my'
    start_urls = ['https://baseball.yahoo.co.jp/npb/']

    def parse(self, response):
        for title in response.xpath('//title/text()'):
            yield { 'title': title.get() }



