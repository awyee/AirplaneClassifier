import scrapy

class AirplaneSpider(scrapy.Spider):
    name = "AirplaneSpider"
    start_urls = [
        'C:\Users\Wintermute-III\Desktop\Aviation Photos _ Latest Photos _ Planespotters.net.html',
    ]

    def parse(self, response):
        yield {'title': response.css('title::text').extract_first()}
        divresponses=response.css('div.PhotoContainer PhotoContainer950')
        for divresponse in divresponses:
            tdresponse=divresponse.css('td.ImgContainer')
            aresponse=tdresponse.css('a::href').extract
            print(aresponse)

            filename = 'links.txt'
            with open(filename, 'wb') as f:
                f.write(aresponse)
