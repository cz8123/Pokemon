from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.forms.models import model_to_dict # 将QuerySet对象转换成字典对象
from collections import OrderedDict
import json, MySQLdb, requests, time, subprocess
from django.urls import reverse
from json.decoder import JSONDecodeError

class PokeDetailView(DetailView):
	queryset = Pokemon.objects.all()
	template_name = 'main.html'
	context_object_name = 'poke_now'
	def get_object(self, queryset=None):
		poke_now = super().get_object(queryset=None)
		self.total = poke_now.hp+poke_now.atk+poke_now.defen+poke_now.satk+poke_now.sdef+poke_now.sp
		self.poke_info = model_to_dict(poke_now)
		self.type1_id = poke_now.type1.id
		self.type2_id = poke_now.type2.id
		self.num = poke_now.num
		return poke_now
	def get_context_data(self, **kw):
		context = super().get_context_data(**kw)
		context.update(self.contextdata())
		return context
	def contextdata(self):
		typeback = Typeback.objects.all()
		poke_field = OrderedDict() # 按顺序保存精灵各项种族值
		for each in Pokemon._meta.local_fields[4:9]: # 因为字典无法切片，要按顺序获取字段名
			poke_field[each.name] = self.poke_info[each.name]
		typelist = []
		typelist.append('t'+str(self.type1_id)) # 获取精灵本身属性的id，对应属性相克表的表头t1~18
		if not (self.type2_id == 19):           # 排除空属性 19
			typelist.append('t'+str(self.type2_id))
		typeatk4 = [] # 4倍弱点
		typeatk2 = []
		typeatk0 = []
		for each in typeback: # 计算属性弱点系数，提取结果为0、2、4的属性
			a = 1
			for t in typelist:
				a = a * (model_to_dict(each)[t])
			if a == 4:
				typeatk4.append(each)
			elif a == 2:
				typeatk2.append(each)
			elif a == 0:
				typeatk0.append(each)
		poke_next = Pokemon.objects.filter(num=(self.num+1))[0] if self.num < 807 else Pokemon.objects.filter(num=1)[0]
		poke_prev = Pokemon.objects.filter(num=(self.num-1))[0] if self.num > 1 else Pokemon.objects.filter(num=807)[0]
		poke_add = Pokemon.objects.filter(num=self.num)
		poke_addition = False
		if len(poke_add) > 1:
			poke_addition = True
		context = {
			'typeatk4': typeatk4,
			'typeatk2': typeatk2,
			'typeatk0': typeatk0,
			'poke_field': poke_field,
			'poke_next': poke_next,
			'poke_prev': poke_prev,
			'total': self.total,
			'poke_add': poke_add,
			'poke_addition': poke_addition,
		}
		return context

def pokepost(request, pk=1):
	poke_now = Pokemon.objects.get(id=pk) # 获取首页pokemon/ 时，是get方法，直接重定向到id=1的实例 
	if request.method == 'POST':
		pk = request.POST.get('pokepost', 1)
		poke_now = Pokemon.objects.get(id=pk)
		return redirect(poke_now)
	return redirect(poke_now)

class MoveDetailView(DetailView):
	queryset = Move.objects.all()
	template_name = 'moves.html'
	context_object_name = 'move'
	def get_object(self, queryset=None):
		move = super().get_object(queryset=None)
		self.pk = move.id
		return move
	def get_context_data(self, **kw):
		context = super().get_context_data(**kw)
		context.update({
			'move_next': Move.objects.get(id=(self.pk+1)) if self.pk < 728 else Move.objects.get(id=1),
			'move_prev': Move.objects.get(id=(self.pk-1)) if self.pk > 1 else Move.objects.get(id=728)
		})
		return context

def movepost(request, pk=1):
	move_now = Move.objects.get(id=pk) # 获取首页moves/ 时，是get方法，直接重定向到id=1的实例 
	if request.method == 'POST': 
		s = request.POST.getlist('s1[]', None)
		pk = request.POST.get('movepost', None)
		if s: # 接收ajax post数据,计算技能打击盲点(0.5、0)
			blind_types = []
			twice_types = []
			if s == None:
				e = False
				f = False
			else:
				if len(s) > 1:
					if not s[1] == '变化':
						move_obj = Typeback.objects.get(name=s[0])
					else:
						move_obj = False
				if move_obj:
					blind_id = []
					twice_id = []
					for i in range(1,19):
						blind_list = []
						blind_list.append(model_to_dict(move_obj)['t'+str(i)])
						if (1 not in blind_list) and (2 not in blind_list):
							blind_id.append(i)
						if (2 in blind_list):
							twice_id.append(i)
					for id_ in blind_id:
						blind_types.append(Types.objects.get(id=id_))
					for id_ in twice_id:
						twice_types.append(Types.objects.get(id=id_))
					f = True
				else:
					f = False
				e = True
			context = {'blind': blind_types, 'twice': twice_types, 'e':e, 'f': f}
			return render(request, 'blind.html', context=context) # 返回模板用于局部更新html
		elif pk:
			move = Move.objects.get(id=pk)
			return redirect(move)
	return redirect(move_now)

# ————————————————————————————————————PGL——————————————————————————————————————————

def check_update(s): # 检查赛季数据是否更新
	url='https://3ds.pokemon-gl.com/frontendApi/gbu/getSeasonPokemon'
	headers={'Referer':'https://3ds.pokemon-gl.com/battel/','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
	form_data={
	'languageId':'9',
	'seasonId':s,
	'battleType':'2',
	'timezone': 'JST',
	'timeStamp': str(int(time.time())),
	}
	r = requests.post(url, data=form_data, headers=headers).text
	try:
		if json.loads(r)['status_code'] == '0000':
			return json.loads(r)['updateDate']
		else:
			return False
	except JSONDecodeError:
		return False

def allpokelist(): # 从数据库获取所有pokemon列表
	database = {'db':'pgl','user':'root', 'passwd':'666666','host':'localhost', 'charset':'utf8'}
	conn = MySQLdb.connect(**database)
	cur = conn.cursor()
	cur.execute('select value from pgl_getSeasonPokemon where name=%s',('pglPokemon',))
	a = cur.fetchall()[0][0]
	poke_dict = OrderedDict()
	poke_list = json.loads(a)['pokemonInfo']
	for each in poke_list:
		poke_dict[each['pokemonId']] = {'name': each['name'], 'monsno': each['monsno']}
	return poke_dict

def ranklist(s, n, rank=None): # 从数据库获取排名, 更新时间
	database = {'db':'pgl','user':'root', 'passwd':'666666','host':'localhost', 'charset':'utf8'}
	conn = MySQLdb.connect(**database)
	cur = conn.cursor()
	cur.execute('select value from pgl_getseasonpokemon where name=%s', ('ranking%s-%s'%(s, n), ))
	rank_list = json.loads(cur.fetchall()[0][0])
	cur.execute('select value from pgl_getseasonpokemon where name=%s', ('updateDate%s'%s, ))
	updateDate = json.loads(cur.fetchall()[0][0])
	if rank:
		return rank_list[:rank], updateDate
	else:
		return rank_list, updateDate

def mysql2dict2(s, n, id_):
	database = {'db':'pgl','user':'root', 'passwd':'666666','host':'localhost', 'charset':'utf8'}
	conn = MySQLdb.connect(**database)
	cur = conn.cursor()
	cur.execute('select value from pgl_getseasonpokemonD_%s_%s where name=%%s'%(s, n),(id_, ))
	a = cur.fetchall()[0][0]
	poke_list = json.loads(a)['rankingPokemonTrend']
	pokeInfo = json.loads(a)['rankingPokemonInfo']
	pokeInfo1 = json.loads(a)
	r = dict()
	if poke_list:
		item_list = poke_list['itemInfo']
		move_list = poke_list['wazaInfo']
		nature_list = poke_list['seikakuInfo']
		ability_list = poke_list['tokuseiInfo']
		item_dict = OrderedDict()
		move_dict = OrderedDict()
		nature_dict = OrderedDict()
		ability_dict = OrderedDict()
		if item_list:
			for each in item_list[:10]:
				if each['name']:
					item_dict[each['ranking']] = {'name':each['name'], 'usageRate':each['usageRate']}
		if move_list:
			for each in move_list[:10]:
				if each['name']:
					move_dict[each['ranking']] = {'name':each['name'], 'usageRate':each['usageRate'], 'model': Move.objects.get(name=each['name'])}
		if nature_list:
			for each in nature_list[:10]:
				if each['name']:
					nature_dict[each['ranking']] = {'name':each['name'], 'usageRate':each['usageRate'], 'detail': Nature.objects.get(name=each['name']).detail}
		if ability_list:
			for each in ability_list:
				if each['name']:
					ability_dict[each['ranking']] = {'name':each['name'], 'usageRate':each['usageRate'], 'detail': Ability.objects.get(name=each['name']).detail}
		r['item_dict'] = item_dict
		r['move_dict'] = move_dict
		r['nature_dict'] = nature_dict
		r['ability_dict'] = ability_dict
		r['pokeInfo'] = pokeInfo
		r['pokeInfo1'] = pokeInfo1
	else:
		r['pokeInfo'] = pokeInfo
		r['pokeInfo1'] = pokeInfo1
	return r

def pgl(request, s='312'):
	if request.method == 'GET':
		seasonid = request.GET.get('season', s)
		rank_list1, updateDate = ranklist(seasonid, '1', 31)
		rank_list2, _ = ranklist(seasonid, '2', 31)
		rank_list5, _ = ranklist(seasonid, '5', 31)
		rank_list6, _ = ranklist(seasonid, '6', 31)
		update = check_update(seasonid) if int(seasonid) >= 312 else None
		is_updated = False
		if update and (update != updateDate):
			is_updated = True
		s = {
				'312': 'Season 12　09/04/18 09:00 AM - 11/06/18 08:59 AM JST　09/04/18 12:00 AM - 11/05/18 11:59 PM UTC',
				'311': 'Season 11　07/10/18 09:00 AM - 09/04/18 08:59 AM JST　07/10/18 12:00 AM - 09/03/18 11:59 PM UTC',
				'310': 'Season 10　05/15/18 09:00 AM - 07/10/18 08:59 AM JST　05/15/18 12:00 AM - 07/09/18 11:59 PM UTC',
				'309': 'Season 9　03/13/18 09:00 AM - 05/15/18 08:59 AM JST　03/13/18 12:00 AM - 05/14/18 11:59 PM UTC',
				'308': 'Season 8　01/23/18 09:00 AM - 03/13/18 08:59 AM JST　01/23/18 12:00 AM - 03/12/18 11:59 PM UTC'
			}
		detail = {
			'312': 'Wcs神战模式，无z，无mega，无宝玉，无画龙点睛',
			'311': 'Special模式，幻兽63单打',
			'310': 'Special模式，反转属性64双打',
			# '309': 'Season 9　03/13/18 09:00 AM - 05/15/18 08:59 AM JST　03/13/18 12:00 AM - 05/14/18 11:59 PM UTC',
			'308': 'Special模式，神战64双打'
		}
		context={
			'rank_list1': rank_list1,
			'rank_list2': rank_list2,
			'rank_list5': rank_list5,
			'rank_list6': rank_list6,
			'updateDate': updateDate,
			'is_updated': is_updated,
			'seasonid': seasonid,
			's': s[seasonid],
			'detail': detail[seasonid],
		}
		# template = 'pglseason%s.html'%seasonid
		template = 'pglseason.html'

	if request.method == 'POST':
		if request.POST.get('load', False):
			id_ = request.POST.get('id')
			seasonid = request.POST.get('seasonid')
			pokelist, _ = ranklist(seasonid, id_)
			context = {'ranklist': pokelist,'id': id_}
			return render(request, 'load.html', context=context)
		else:
			p_id = request.POST.get('id')
			typeid = request.POST.get('typeid')
			seasonid = request.POST.get('seasonid')
			r = mysql2dict2(seasonid, typeid, p_id)
			allpoke_dict = allpokelist()
			try: # 先按照pgl编号寻找pokemon模型, 如果DoesNotExist, 再按照名字选取第一个符合的模型
				pokemodel = Pokemon.objects.get(pic=r['pokeInfo']['pokemonId'])
			except Pokemon.DoesNotExist:
				pokemodel = Pokemon.objects.filter(name=r['pokeInfo']['name'])[0]

			abili = OrderedDict()
			for i in ['hp', 'atk', 'defen', 'satk', 'sdef', 'sp']:
				abili[i] = getattr(pokemodel, i, None) # eval('pokemodel.%s'%i)

			total= pokemodel.hp+pokemodel.atk+pokemodel.defen+pokemodel.satk+pokemodel.sdef+pokemodel.sp

			type1 = Types.objects.get(pgl_typeid=r['pokeInfo']['typeId1'])
			if r['pokeInfo']['typeId2'] and (0<r['pokeInfo']['typeId2']<19):
				type2 = Types.objects.get(pgl_typeid=r['pokeInfo']['typeId2'])
			else:
				type2 = None
			if typeid == '1':
				type_ = 'Single'
			elif typeid == '2':
				type_ = 'Double'
			elif typeid == '5':
				type_ = 'Special'
			elif typeid == '6':
				type_ = 'Wcs'
			else:
				type_ = 'Special'
			s1 = {'312': 'Season 12', '311': 'Season 11', '310': 'Season 10', '309': 'Season 9', '308': 'Season 8'}
			context = {
				'p_id': p_id,
				'item_dict': r.get('item_dict', None),
				'move_dict': r.get('move_dict', None),
				'nature_dict': r.get('nature_dict', None),
				'ability_dict': r.get('ability_dict', None),
				'allpoke_dict': allpoke_dict,
				'poke_now': r['pokeInfo'],
				'pokeInfo': r['pokeInfo1'],
				'typeid': typeid,
				'type_': type_,
				's': s1[seasonid],
				'pokemodel': pokemodel,
				'seasonid': seasonid,
				'type1': type1,
				'type2': type2,
				'abili': abili,
				'total': total,
			}
			return render(request, 'pokedetail.html', context=context)
	return render(request, template, context=context)