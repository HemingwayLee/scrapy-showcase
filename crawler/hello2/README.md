# First
* Use `shell` to check
```
scrapy shell 'https://baseball.yahoo.co.jp/npb/'
```

## CSS selector and xpath selector
* CSS selectors are converted to XPath under-the-hood
```
>>> response.css('title')
[<Selector xpath='descendant-or-self::title' data='<title>プロ野球 - スポーツナビ</title>'>]
>>> response.xpath('//title/text()').get()
'プロ野球 - スポーツナビ'
```




