from ..models import Pokemon
from django import template
import MySQLdb, json



register = template.Library()

@register.simple_tag
def get_pokemons():
	database = {'db':'poke','user':'root', 'passwd':'666666','host':'localhost', 'charset':'utf8'}
	conn = MySQLdb.connect(**database)
	cur = conn.cursor()
	cur.execute('SELECT id, name FROM poke_pokemon WHERE id IN (SELECT min(id) FROM poke_pokemon group by num) order by num')
	b = []
	for each in cur.fetchall():
		b.append({'id': each[0], 'name': each[1]})
	return b

# @register.simple_tag
# def get_pokemons():
# 	b = []
# 	for each in Pokemon.objects.all():
# 		b.append({'id': each.id, 'name': each.name})
# 	return b