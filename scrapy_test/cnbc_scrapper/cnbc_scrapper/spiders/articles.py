import scrapy
from scrapy.exceptions import CloseSpider


class ArticlesSpider(scrapy.Spider):
    name = "articles"

    counter = 0

    def start_requests(self):
        urls = [
            "https://www.cnbc.com/finance/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):


        link = response.css('div#SectionWithNativeTVE-LoadMore-15 a::attr(href)').get()


        if link is None:
            raise CloseSpider("No more pages")
        
        self.counter += 1

        if self.counter > 100:
            raise CloseSpider("Max number of pages reached")


        print("this is the link: " + link)

        yield scrapy.Request(link, callback=self.parse)


