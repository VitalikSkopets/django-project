from django import template
from shop.models import *

register = template.Library()


# пользовательский простой тег, который возвращает коллекцию данных из БД - список типов ТС
@register.simple_tag(name='get_types')
def get_types(param=None):
    if not param:
        return Type.objects.all()
    else:
        return Type.objects.filter(pk=param)


# пользовательский включайщий тег, который возвращает фрагмент HTML-страницы в который, в свою очередь по ключу "types"
# передается в качестве пареметра коллекция данных из БД - список типов ТС
@register.inclusion_tag('shop/includes/list_types.html', '')
def show_types(sort=None):
    types_dict = {}
    if not sort:
        vehicles_types = Type.objects.all()
    else:
        vehicles_types = Type.objects.order_by(sort)
    for vehicle_type in vehicles_types:
        vehicle_count = Vehicle.objects.filter(type__title=vehicle_type).count()
        types_dict[vehicle_type] = vehicle_count
    return {"vehicles_types": vehicles_types,
            'types_dict': types_dict,
            }
