from .spiders import PlaneSpider,PlaneSpider2

if __name__=="__main__":
    searchcrawler=PlaneSpider()
    searchcrawler.parse()
    planecrawler=PlaneSpider2()
    planecrawler.parse()