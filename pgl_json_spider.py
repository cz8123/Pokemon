import requests, json, MySQLdb, time
# from collections import OrderedDict
from multiprocessing import Pool
# from functools import partial

headers={'Referer':'https://3ds.pokemon-gl.com/battel/','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
database = {'db':'pgl','user':'root', 'passwd':'666666','host':'localhost', 'charset':'utf8'}

latest_season = '310'

def getallPokemon(): # 所有pokemon列表
	conn = MySQLdb.connect(**database)
	cur = conn.cursor()
	url='https://3ds.pokemon-gl.com/frontendApi/master/getPokemon'
	form_data={
	'languageId':'9',
	'timezone': 'JST',
	'timeStamp': str(int(time.time())),
	}
	r = requests.post(url, data=form_data, headers=headers).text
	status_code = json.loads(r)['status_code']
	if status_code == '0000':
		# cur.execute('insert into pgl_getSeasonPokemon (name, value) values (%s, %s)',('pglPokemon', r))
		cur.execute('update pgl_getSeasonPokemon set value=%s where name=%s',(r, 'pglPokemon'))
		conn.commit()
		cur.close()
		conn.close()

def update_Date(s): # 赛季更新时间
	conn = MySQLdb.connect(**database)
	cur = conn.cursor()
	url='https://3ds.pokemon-gl.com/frontendApi/gbu/getSeasonPokemon'
	form_data={
	'languageId':'9',
	'seasonId':s,
	'battleType':'2',
	'timezone': 'JST',
	'timeStamp': str(int(time.time())),
	}
	r = requests.post(url, data=form_data, headers=headers).text
	status_code = json.loads(r)['status_code']
	if status_code == '0000':
		updateDate = json.loads(r)['updateDate']
		cur.execute('update pgl_getSeasonPokemon set value=%s where name=%s',(json.dumps(updateDate), 'updateDate%s'%s))
		# cur.execute('insert into pgl_getSeasonPokemon (name, value) values (%s, %s)',('updateDate%s'%s, json.dumps(updateDate)))
		conn.commit()
		cur.close()
		conn.close()

def allranklist(s, n): # 所有有排名的pokemon
	conn = MySQLdb.connect(**database)
	cur = conn.cursor()
	cur.execute('select value from pgl_getseasonpokemond_%s_%s'%(s, n))
	a = cur.fetchall()
	rank_list = []
	for each in a:
		poke = json.loads(each[0])['rankingPokemonInfo']
		if poke['ranking'] != 0:
			rank_list.append({'id':poke['pokemonId'], 'name':poke['name'], 'rank':poke['ranking']})
	rank_list = sorted(rank_list, key=lambda x: x['rank'])

	cur.execute('update pgl_getSeasonPokemon set value=%s where name=%s', (json.dumps(rank_list), 'ranking{}-{}'.format(s, n)))
	# cur.execute('insert into pgl_getSeasonPokemon (name, value) values (%s, %s)', ('ranking{}-{}'.format(s, n), json.dumps(rank_list)))
	conn.commit()
	cur.close()
	conn.close()


def getSeasonPokemonDetail(id_, s=latest_season): # pokemon详情
	conn = MySQLdb.connect(**database)
	cur = conn.cursor()
	detail_url='https://3ds.pokemon-gl.com/frontendApi/gbu/getSeasonPokemonDetail'
	for n in ['1', '2', '5', '6']:
		form_data={
		'languageId':'9',
		'seasonId':s,
		'battleType':n,
		'pokemonId':id_,
		'displayNumberWaza': '10',
		'displayNumberTokusei': '4',
		'displayNumberSeikaku': '10',
		'displayNumberItem': '10',
		'timezone': 'JST',
		'timeStamp': str(int(time.time())),
		}
		r = requests.post(detail_url, data=form_data, headers=headers)
		detail_list = r.text
		cur.execute('insert into pgl_getseasonpokemond_%s_%s (name, value) values (%%s, %%s)'%(s, n), (id_, detail_list))
	conn.commit()



if __name__ == '__main__':
	getallPokemon()
	conn = MySQLdb.connect(**database)
	cur = conn.cursor()
	cur.execute('select value from pgl_getseasonpokemon where name=%s',('pglPokemon',))
	a = cur.fetchall()
	b = json.loads(a[0][0])['pokemonInfo']
	list_ = (each['pokemonId'] for each in b)
	for n in ['1', '2', '5', '6']:
		cur.execute('truncate table pgl_getseasonpokemond_%s_%s'%(latest_season, n))
		conn.commit()
	with Pool() as p:
		r = p.map(getSeasonPokemonDetail, list_)
	for n in ['1', '2', '5', '6']:
		allranklist(s=latest_season, n=n)
	update_Date(s=latest_season)
	cur.close()
	conn.close()
