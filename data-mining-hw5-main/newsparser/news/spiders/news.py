import scrapy
from scrapy.http import HtmlResponse
from news.items import NewsItem
from scrapy.loader import ItemLoader


class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["mail.ru"]
    start_urls = ["https://news.mail.ru"] # ищем товары в категории Книги

    def parse(self, response):
        xpath_text = '''
            //a[contains(@href, "news.mail.ru")
              or contains(@href, "pogoda.mail.ru")
              or contains(@href, "finance.mail.ru")
              or contains(@href, "vfokuse.mail.ru")]/@href
        '''
        news_links = response.xpath(xpath_text).getall() 
        print(response.status, response.url)
        for link in news_links:
            yield response.follow(link, callback=self.news_parse) # перейти по ссылке
    
    def news_parse(self, response):
        header = response.xpath("//h1[@class='hdr__inner']/text()").get() 
        print(header)
        source = response.xpath("//span[@class='link__text']/text()").get() 
        print(source)
        datetime = response.xpath("//span[contains(@class, 'js-ago')]/@datetime").get() 
        print(datetime)
        url = response.url
        yield NewsItem(header=header, source=source, datetime=datetime, url=url)
