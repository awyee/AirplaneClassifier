#File to scrape Planespotters.net

import scrapy as spy

starturl='https://www.planespotters.net/photo/search?subtype=747-400'

class PictureSpider(scrapy.Spider):
    picname=scrapy.Field()
    planetype=scrapy.Field()
    url=scrapy.Field()

if __name__=="__main__":
