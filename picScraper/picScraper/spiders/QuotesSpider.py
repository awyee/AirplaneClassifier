import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        yield {'title': response.css('title::text').extract_first()}
        #for quote in response.css('div.quote'):
        #    yield {
        #        'text': quote.css('span.text::text').extract_first(),
        #        'author': quote.css('small.author::text').extract_first(),
        #        'tags': quote.css('div.tags a.tag::text').extract(),
        #    }