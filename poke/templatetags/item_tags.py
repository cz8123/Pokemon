from ..models import Item, Items
from django import template

register = template.Library()

@register.simple_tag
def get_items():
    return Items.objects.all()