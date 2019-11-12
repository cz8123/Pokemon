# -*- coding: utf-8 -*-
import scrapy
from poke_spider.items import PokeSpiderItem

class PokemonSpider(scrapy.Spider):
    name = "pokemon"
    allowed_domains = ["52poke.com"]
    start_urls = ['https://wiki.52poke.com/wiki/%E5%AE%9D%E5%8F%AF%E6%A2%A6%E5%88%97%E8%A1%A8%EF%BC%88%E6%8C%89%E5%85%A8%E5%9B%BD%E5%9B%BE%E9%89%B4%E7%BC%96%E5%8F%B7%EF%BC%89/%E7%AE%80%E5%8D%95%E7%89%88']

    def parse(self, response):
        table = response.xpath('//table[starts-with(@class,"a-c")]')
        for href in table.xpath('tr/td/a/@href').extract()[::3]:
	        next_page = response.urljoin(href)
	        yield scrapy.Request(next_page,callback=self.parse2)

    def parse2(self,response):
        name = response.xpath('//h1[@id="firstHeading"]/text()').extract()[0]
        # url = response.xpath('//img[@width>=250]/@data-url').extract()[0]
        # url = response.xpath('//img[@width<250 and @width>=100]/@data-url').extract()
        # url = response.xpath('//img[@width>=250]/@data-url').extract()[2:]
        # image_url = []
        # for each in url:
        #     image_url.append('http:' + each)
        # image_url = ['http:'+ url]
        t1_1 = response.xpath('//td[@style="border:1px solid#D8D8D8"]/a/text()').extract()
        t1_2 = response.xpath('//td[@style="border:1px solid#D8D8D8"]/b/a/text()').extract()
        t1_3 = response.xpath('//td[@style="border:1px solid#D8D8D8"]/i/a/text()').extract()
        t2_1 = response.xpath('//td[@style="border:1px solid #D8D8D8"]/a/text()').extract()
        t2_2 = response.xpath('//td[@style="border:1px solid #D8D8D8"]/b/a/text()').extract()
        t2_3 = response.xpath('//td[@style="border:1px solid #D8D8D8"]/i/a/text()').extract()
        t3_1 = response.xpath('//td[@style="border: 1px solid #D8D8D8"]/a/text()').extract()
        t3_2 = response.xpath('//td[@style="border: 1px solid #D8D8D8"]/b/a/text()').extract()
        t3_3 = response.xpath('//td[@style="border: 1px solid #D8D8D8"]/i/a/text()').extract()
        t = list(set(t1_1+t1_2+t1_3+t2_1+t2_2+t2_3+t3_1+t3_2+t3_3))
        move = []
        for each in t:
        	if not each.startswith('招式学习'):
        		move.append(each)
        item = PokeSpiderItem()
        # item['img_url'] = image_url
        # item['img_url'] = image_url
        item['name'] = name
        item['moves'] = move
        yield item
