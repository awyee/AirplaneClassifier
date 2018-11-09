import scrapy
class PlanePicItem(scrapy.Item):
     images = scrapy.Field()
     image_urls = scrapy.Field()
class AirplaneSpider2(scrapy.Spider):
    name = "AirplaneSpider2"
    start_urls = [
        'https://www.planespotters.net/photo/890367/n706ck-kalitta-air-boeing-747-4b5f',
    ]

    def parse(self, response):
        #yield {'Title': response.xpath('//title/text()').extract()}
        piclinks=response.xpath("//img/@src").extract_first()

        #links=response.xpath('//div//table//tr//td/a/@href').extract()
        filename = 'piclinks.txt'
        with open(filename, 'a') as f:
            f.write(piclinks+'\n')
        PlanePic=PlanePicItem()
        PlanePic["image_urls"]=[piclinks]
        return PlanePic