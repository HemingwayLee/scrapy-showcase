import scrapy

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    base_url = 'http://ec2-54-238-101-61.ap-northeast-1.compute.amazonaws.com/'
    start_urls = [base_url]

    def parse(self, response):
        for title in response.xpath('//title/text()'):
            yield { 'title': title.get() }

        for panel in response.css('.my_panel'):
            addr = panel.xpath('@onclick').get()
            if addr:
                page = addr[addr.find("'")+1:addr.rfind("'")]
                # print("!!!!!!!")
                # print(page)
                
                next_page_url = self.base_url + page
                request = scrapy.Request(url=next_page_url, callback=self.parse)
                yield request

