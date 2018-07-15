from ..models import Move
from django import template
import MySQLdb, json

register = template.Library()

@register.simple_tag
def get_moves():
    return Move.objects.all()

@register.filter(name='get_detail')
def get_detail(id):
    database = {'db':'poke','user':'root', 'passwd':'666666','host':'localhost', 'charset':'utf8'}
    conn = MySQLdb.connect(**database)
    cur = conn.cursor()
    cur.execute('SELECT value FROM poke_move_json where id=%s', (id,))
    detail = json.loads(cur.fetchall()[0][0])
    return detail