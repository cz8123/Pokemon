# -*- coding: utf-8 -*-
import scrapy, re
from poke_spider.items import PokeSpiderItem

class PokemonSpider(scrapy.Spider):
    name = "pokemon1"
    allowed_domains = ["52poke.com"]
    start_urls = ['https://wiki.52poke.com/wiki/%E5%AE%9D%E5%8F%AF%E6%A2%A6%E5%88%97%E8%A1%A8%EF%BC%88%E6%8C%89%E5%85%A8%E5%9B%BD%E5%9B%BE%E9%89%B4%E7%BC%96%E5%8F%B7%EF%BC%89/%E7%AE%80%E5%8D%95%E7%89%88']

    def parse(self, response):
        table = response.xpath('//table[starts-with(@class,"a-c")]')
        for href in table.xpath('tr/td/a/@href').extract()[::3]:
	        next_page = response.urljoin(href)
	        yield scrapy.Request(next_page,callback=self.parse2)

    def parse2(self,response):
        # name = response.xpath('//h1[@id="firstHeading"]/text()').extract()[0]
        # url = response.xpath('//img[@width>=250]/@data-url').extract()[0]
        # url = response.xpath('//img[@width<250 and @width>=100]/@data-url').extract()
        url = response.xpath('//img[@width>=250]/@data-url').extract()[1:]
        image_url = []
        for i in url:
            b = re.compile(r'png/(.*?)px')
            try:
                image_url.append('http:'+ b.sub('png/400px', i))
            except:
                continue
        # image_url = ['http:'+ url]
        item = PokeSpiderItem()
        item['img_url'] = image_url
        # item['name'] = name
        yield item
