import aiohttp, asyncio, time, aiomysql, MySQLdb, json

headers={'Referer':'https://3ds.pokemon-gl.com/battel/','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
database = {'db':'pgl','user':'root', 'passwd':'666666','host':'localhost', 'charset':'utf8'}
latest_season = '311'

async def create_pool(loop):
	pool = await aiomysql.create_pool(
			host='localhost', port=3306, user='root',
			password='666666', db='pgl', charset='utf8',
			autocommit=True, loop=loop
		)
	return pool

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
		cur.execute('update pgl_getseasonpokemon set value=%s where name=%s',(r, 'pglPokemon'))
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
		cur.execute('update pgl_getseasonpokemon set value=%s where name=%s',(json.dumps(updateDate), 'updateDate%s'%s))
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

	cur.execute('update pgl_getseasonpokemon set value=%s where name=%s', (json.dumps(rank_list), 'ranking{}-{}'.format(s, n)))
	# cur.execute('insert into pgl_getSeasonPokemon (name, value) values (%s, %s)', ('ranking{}-{}'.format(s, n), json.dumps(rank_list)))
	conn.commit()
	cur.close()
	conn.close()

async def getDetail(id_, loop):
	detail_url='https://3ds.pokemon-gl.com/frontendApi/gbu/getSeasonPokemonDetail'
	form_data={
	'languageId':'9',
	'seasonId':'311',
	'battleType':'6',
	'pokemonId':id_,
	'displayNumberWaza': '10',
	'displayNumberTokusei': '4',
	'displayNumberSeikaku': '10',
	'displayNumberItem': '10',
	'timezone': 'JST',
	'timeStamp': str(int(time.time())),
	}
	async with aiohttp.ClientSession() as session:
		async with session.post(detail_url, headers=headers, data=form_data, timeout=60) as r:
			detail_list = await r.text()
	pool = await create_pool(loop=loop)
	async with pool.get() as conn:
		async with conn.cursor() as cur:
			await cur.execute('insert into linshi (name, value) values (%s, %s)', (id_, detail_list))
	pool.close()
	await pool.wait_closed()


conn = MySQLdb.connect(**database)
cur = conn.cursor()
cur.execute('select value from pgl_getseasonpokemon where name=%s',('pglPokemon',))
a = cur.fetchall()
cur.execute('truncate table linshi')
conn.commit()
cur.close()
conn.close()

b = json.loads(a[0][0])['pokemonInfo']
list_ = [each['pokemonId'] for each in b]

for i in range(0, 9):
	loop = asyncio.get_event_loop()
	tasks = [getDetail(id_, loop=loop) for id_ in list_[i*100:(i+1)*100]]
	loop = asyncio.get_event_loop()
	loop.run_until_complete(asyncio.wait(tasks))
	
loop.close()





