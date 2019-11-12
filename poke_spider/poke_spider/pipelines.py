# -*- coding: utf-8 -*-

from io import BytesIO, StringIO
from scrapy.pipelines.images import ImagesPipeline
import MySQLdb, scrapy
from PIL import Image

class DXCPipeline(object): # 大学城图片
	def process_item(self, item, spider):
		name = item['name']
		folder = item['folder']
		img = item['body']
		with open('%s/%s'%(folder, name), 'wb') as f:
			f.write(img)

class ShowdownPipeline(object): # showdown
    def process_item(self, item, spider):
        name = item['name']
        folder = item['folder']
        img = item['body']
        with open('%s/%s'%(folder, name), 'wb') as f:
            f.write(img)

class PglPipeline(ImagesPipeline): # pgl图片
    def get_media_requests(self, item, info):
        for each in item['image_urls']:
            yield scrapy.Request(each, meta={'item':item})
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        file = item['name']
        return 'full1/%s'%file
    def convert_image(self, image, size=None):
        buf = BytesIO()
        image.save(buf, 'PNG')
        return image, buf

class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for each in item['img_url']:
            yield scrapy.Request(each,meta={'item': item})

    def file_path(self, request, response=None, info=None):
    	item = request.meta['item']
    	image_guid = item['name']+'.png'
    	return 'full/%s' % (image_guid)        

    def convert_image(self, image, size=None):
        buf = BytesIO()
        image.save(buf, 'PNG')
        return image, buf

class WikiPipeline(ImagesPipeline): # wiki图片
    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('/')[-1]
        return 'full1/%s' % (image_guid)        

    def convert_image(self, image, size=None):
        buf = BytesIO()
        image.save(buf, 'PNG')
        return image, buf

class MovesPipeline(object): # moves
    def process_item(self, item, spider):
    	database = {'db':'poke','user':'root', 'passwd':'666666','host':'localhost', 'charset':'utf8'}
    	conn = MySQLdb.connect(**database)
    	cur = conn.cursor()
    	cur.execute('select num from poke_pokemon where name=%s', (item['name'],))
    	poke_num = cur.fetchall()[0][0]
    	cur.execute('select id from poke_pokemon where num=%s', (poke_num,))
    	id_ = cur.fetchall()
    	pokemon_id = []
    	for each in id_:
    		pokemon_id.append(each[0])
    	moveid_list = []
    	for each in item['moves']:
    		cur.execute('select id from poke_move where name=%s', (each,))
    		result = cur.fetchall()
    		if not result:
    			continue
    		move_id = result[0][0]
    		moveid_list.append(move_id)
    	for x in pokemon_id:
	    	for y in moveid_list:
	    		cur.execute('insert into poke_pokemon_move (pokemon_id, move_id) values (%s, %s)', (x, y))
    	conn.commit()
    	cur.close()
    	conn.close()
    	return item
