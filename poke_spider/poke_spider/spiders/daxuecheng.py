# -*- coding: utf-8 -*-
import scrapy
from poke_spider.items import PokeSpiderItem

class PokemonSpider(scrapy.Spider):
    name = "pokemon1"
    # allowed_domains = ["52poke.com"]
    # start_urls = ['http://s.pokeuniv.com/pokemon/sprite/front/%s.gif'%i for i in range(1,808)]+\
    #             ['http://s.pokeuniv.com/pokemon/sprite/front-shiny/%s.gif'%i for i in range(1,808)]+\
    #             ['http://s.pokeuniv.com/pokemon/sprite/front/%s.1.gif'%i for i in range(1,808)]+\
    #             ['http://s.pokeuniv.com/pokemon/sprite/front-shiny/%s.1.gif'%i for i in range(1,808)]+\
    #             ['http://s.pokeuniv.com/pokemon/sprite/front/%s.2.gif'%i for i in range(1,808)]+\
    #             ['http://s.pokeuniv.com/pokemon/sprite/front-shiny/%s.2.gif'%i for i in range(1,808)]
    # start_urls = ['http://s.pokeuniv.com/pokemon/icon/%s.png'%i for i in range(1,808)]+\
    #             ['http://s.pokeuniv.com/pokemon/icon/%s.1.png'%i for i in range(1,808)]+\
    #             ['http://s.pokeuniv.com/pokemon/icon/%s.2.png'%i for i in range(1,808)]
    start_urls = ['http://s.pokeuniv.com/pokemon/sprite/front-shiny/%s.%s.gif'%(i, j) for i in [25,201,351,386,479,493,585,586,649,664,665,666,669,670,671,676,710,711,741,773,774,800] for j in range(3,28)]
    # start_urls = ['http://s.pokeuniv.com/pokemon/pgl/%s.1.png'%i for i in range(1,808)]+\
                # ['http://s.pokeuniv.com/pokemon/pgl/%s.2.png'%i for i in range(1,808)]
    # def parse(self, response): # gif
    #     body = response.body
    #     url = response.url
    #     five = url.split('/')[5]
    #     six = url.split('/')[6].split('.')[1]
    #     if five == 'front':
    #         folder = 'front'
    #     elif five == 'front-shiny':
    #         folder = 'front-shiny'

    #     name = url.split('/')[6]
    #     item = PokeSpiderItem()
    #     item['body'] = body
    #     item['name'] = name
    #     item['folder'] = folder
    #     yield item

    def parse(self, response): # icon、pgl
        body = response.body
        url = response.url
        name = url.split('/')[6]
        folder = 'icon'
        item = PokeSpiderItem()
        item['body'] = body
        item['name'] = name
        item['folder'] = folder
        yield item


        
        
        
