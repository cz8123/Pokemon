from django.db import models
from django.urls import reverse

class Types(models.Model): # 18种属性模型
	name = models.CharField(max_length=10)
	color = models.CharField(max_length=20)
	pgl_typeid = models.IntegerField(blank=True) # 对应pgl 的typeid
	def __str__(self):
		return self.name

class Typeback(models.Model): # 属性克制表（列为防御方属性）
	name = models.CharField(max_length=10)
	typeatk = models.ForeignKey(Types, blank=True, on_delete=models.CASCADE)
	t1 = models.FloatField()
	t2 = models.FloatField()
	t3 = models.FloatField()
	t4 = models.FloatField()
	t5 = models.FloatField()
	t6 = models.FloatField()
	t7 = models.FloatField()
	t8 = models.FloatField()
	t9 = models.FloatField()
	t10 = models.FloatField()
	t11 = models.FloatField()
	t12 = models.FloatField()
	t13 = models.FloatField()
	t14 = models.FloatField()
	t15 = models.FloatField()
	t16 = models.FloatField()
	t17 = models.FloatField()
	t18 = models.FloatField()
	def __str__(self):
		return self.name

class Cate(models.Model):
	name = models.CharField(max_length=10)
	color = models.CharField(max_length=20)
	def __str__(self):
		return self.name

class Nature(models.Model):
	name = models.CharField(max_length=10)
	detail = models.CharField(max_length=20)
	def __str__(self):
		return self.name

class Ability(models.Model):
	name = models.CharField(max_length=20)
	detail = models.TextField()
	def __str__(self):
		return self.name

class MoveRange(models.Model):
	name = models.CharField(max_length=30)
	d1 = models.CharField(max_length=10, default='#f4481d')
	d2 = models.CharField(max_length=10, default='#f4481d')
	d3 = models.CharField(max_length=10, default='#f4481d')
	z = models.CharField(max_length=10, default='#f4481d')
	t1 = models.CharField(max_length=10, default='#f4481d')
	t2 = models.CharField(max_length=10, default='#769ad0')
	def __str__(self):
		return self.name

class Move(models.Model):
	name = models.CharField(max_length=20)
	power = models.CharField(max_length=10)
	z_power = models.CharField(max_length=10, blank=True)
	accuracy = models.CharField(max_length=10)
	pp = models.CharField(max_length=10)
	priority = models.CharField(max_length=10)
	detail = models.TextField()
	types = models.ForeignKey(Types, blank=True, on_delete=models.CASCADE)
	cate = models.ForeignKey(Cate, blank=True, on_delete=models.CASCADE)
	move_range = models.ForeignKey(MoveRange, blank=True, on_delete=models.CASCADE)
	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('poke:moves', kwargs={'pk': self.pk})

class Item(models.Model):
	itemid = models.IntegerField()
	name = models.CharField(max_length=20)
	detail = models.TextField()
	def __str__(self):
		return self.name

class Items(models.Model):
	itemid = models.IntegerField()
	name = models.CharField(max_length=20)
	name_en = models.CharField(max_length=20)
	detail = models.TextField()
	def __str__(self):
		return self.name

class Pokemon(models.Model):
    num = models.IntegerField()
    name = models.CharField(max_length=10)
    name1 = models.CharField(max_length=20, blank=True)
    name_en = models.CharField(max_length=30, blank=True)
    hp = models.PositiveSmallIntegerField()
    atk = models.PositiveSmallIntegerField()
    defen = models.PositiveSmallIntegerField()
    satk = models.PositiveSmallIntegerField()
    sdef = models.PositiveSmallIntegerField()
    sp = models.PositiveSmallIntegerField()
    type1 = models.ForeignKey(Types, blank=True, related_name='type1', on_delete=models.CASCADE)
    type2 = models.ForeignKey(Types, blank=True, related_name='type2', on_delete=models.CASCADE)
    ability1 = models.ForeignKey(Ability, blank=True, related_name='ability1', on_delete=models.CASCADE)
    ability2 = models.ForeignKey(Ability, blank=True, related_name='ability2', on_delete=models.CASCADE)
    ability3 = models.ForeignKey(Ability, blank=True, related_name='ability3', on_delete=models.CASCADE)
    pic = models.CharField(max_length=20, blank=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
    	return reverse('poke:index', kwargs={'pk':self.pk})









