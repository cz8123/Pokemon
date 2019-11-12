from django.contrib import admin
from .models import *

# class PokeAdmin(admin.ModelAdmin):
# 	list_display = ['num', 'name','hp', 'atk', 'defen', 'satk', 'sdef', 'sp', 'ability2']
# 	search_fields = ['num', 'name']

# class AbilityAdmin(admin.ModelAdmin):
# 	list_display = ['id', 'name','detail']
# 	search_fields = ['name']

# class MoveAdmin(admin.ModelAdmin):
# 	list_display = ['id', 'name','power', 'z_power', 'accuracy', 'pp', 'priority', 'types', 'cate']
# 	list_filter=['priority']
# 	search_fields=['name']

# admin.site.register(Pokemon, PokeAdmin)
# admin.site.register(Ability, AbilityAdmin)
# admin.site.register(Move, MoveAdmin)
# admin.site.register([Types, Cate])
