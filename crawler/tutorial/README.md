# How
```
scrapy startproject tutorial
scrapy crawl aaa
```

## Debug
* After running 
```
telnet 127.0.0.1 6023
```

* [Reference](https://docs.scrapy.org/en/latest/topics/telnetconsole.html)

# Shell
* shell
```
scrapy shell 'http://quotes.toscrape.com/page/1/'
```

* result
```
[s] Available Scrapy objects:
[s]   scrapy     scrapy module (contains scrapy.Request, scrapy.Selector, etc)
[s]   crawler    <scrapy.crawler.Crawler object at 0x112e2f760>
[s]   item       {}
[s]   request    <GET http://quotes.toscrape.com/page/1/>
[s]   response   <200 http://quotes.toscrape.com/page/1/>
[s]   settings   <scrapy.settings.Settings object at 0x112e2fdf0>
[s]   spider     <DefaultSpider 'default' at 0x1132db250>
[s] Useful shortcuts:
[s]   fetch(url[, redirect=True]) Fetch URL and update local objects (by default, redirects are followed)
[s]   fetch(req)                  Fetch a scrapy.Request and update local objects 
[s]   shelp()           Shell help (print this help)
[s]   view(response)    View response in a browser
>>> response
<200 http://quotes.toscrape.com/page/1/>
>>> response.css('title')
[<Selector xpath='descendant-or-self::title' data='<title>Quotes to Scrape</title>'>]
>>> response.css('title').getall()
['<title>Quotes to Scrape</title>']
>>> response.xpath('//title/text()').get()
'Quotes to Scrape'
```

