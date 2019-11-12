# -*- coding: utf-8 -*-
import scrapy
from poke_spider.items import PokeSpiderItem

class PokemonSpider(scrapy.Spider):
    name = "showdown"
    # allowed_domains = ["52poke.com"]
    start_urls = ['http://play.pokemonshowdown.com/sprites/xyani/',
    			'http://play.pokemonshowdown.com/sprites/xyani-shiny/',
    			'http://play.pokemonshowdown.com/sprites/xyani-shiny-back/',
    			'http://play.pokemonshowdown.com/sprites/xyani-back/',
    			'http://play.pokemonshowdown.com/sprites/xyani-back-shiny/']
    def parse(self, response):
    	folder = response.url.split('/')[4]
    	meta = {'folder': folder}
    	for href in response.xpath('//tr/td/a/@href')[1:]:
            yield response.follow(href, callback=self.parse2, meta=meta)
    def parse2(self, response):
    	folder = response.meta['folder']
    	body = response.body
    	name = response.url.split('/')[5]
    	item = PokeSpiderItem()
    	item['name'] = name
    	item['body'] = body
    	item['folder'] = folder
    	yield item




        
        
        
