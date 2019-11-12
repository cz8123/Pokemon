# -*- coding: utf-8 -*-
import scrapy
from pgl.items import PglItem

class PglPicSpider(scrapy.Spider):
    name = 'pgl_pic'
    allowed_domains = ['pokemon-gl.com']
    # start_urls = ['https://n-3ds-pgl-contents.pokemon-gl.com/share/images/pokemon/300/code.png']
    def start_requests(self): # pokemon
        for i in range(801, 802):
            for j in range(1,28):
                yield scrapy.Request('https://n-3ds-pgl-contents.pokemon-gl.com/share/images/pokemon/300/%s.png'%\
                str(hex(0x1000000|0x159a55e5*(i + j*0x10000)&0xFFFFFF))[3:], callback=self.parse, 
                meta={'name':str(i) + '-' + str(j) + '.png'})
    # def start_requests(self): # item
    #     for i in range(1000):
    #         yield scrapy.Request('https://n-3ds-pgl-contents.pokemon-gl.com/share/images/item/%s.png'%\
    #             str(hex(0x1000000|0x159a55e5*(i+0*0x10000)&0xFFFFFF))[3:], callback=self.parse, 
    #             meta={'name':str(i) + '.png'})
    def parse(self, response):
        name = response.meta['name']
        item = PglItem()
        item['image_urls'] = [response.url]
        item['name'] = name
        yield item
