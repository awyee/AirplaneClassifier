import scrapy


class PlanePicItem(scrapy.Item):
    images = scrapy.Field()
    image_urls = scrapy.Field()

class AirplaneSpider(scrapy.Spider):
    name = "AirplaneSpider"
    start_urls = [
        'https://www.planespotters.net/photo/search?actype=s_A320-200',
    ]
    page=1
    def parse(self, response):
        #yield {'Title': response.xpath('//title/text()').extract()}
        self.links=response.xpath("//a[@target='_self']/@href").extract()

        #links=response.xpath('//div//table//tr//td/a/@href').extract()
        filename = 'links_A320.txt'
        for link_no, link in enumerate(self.links):
            self.links[link_no]='https://www.planespotters.net'+link.split('?')[0]
            pic_request= scrapy.Request(self.links[link_no],callback=self.parse_pic_page)
            yield pic_request
        with open(filename, 'a') as f:
            for link in self.links:
                f.write(link+'\n')

        self.nextlink=response.xpath("//a[@rel='next']/@href").extract_first()
        self.page = self.page + 1
        if self.nextlink is not None and self.page<70:
            self.nextlink = response.urljoin(self.nextlink)
            yield scrapy.Request(self.nextlink, callback=self.parse)


    def parse_pic_page(self, response):
        #yield {'Title': response.xpath('//title/text()').extract()}
        piclinks=response.xpath("//img/@src").extract_first()

        #links=response.xpath('//div//table//tr//td/a/@href').extract()
        filename = 'piclinks_A320.txt'
        with open(filename, 'a') as f:
            f.write(piclinks+'\n')
        PlanePic=PlanePicItem()
        PlanePic["image_urls"]=[piclinks]
        return PlanePic