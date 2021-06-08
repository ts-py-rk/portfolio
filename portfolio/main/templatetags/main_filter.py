# from django.utils.safestring import mark_safe
from django.template import Library

register = Library()

@register.filter('get_value_from_dict')
def get_value_from_dict(dict_data, key):
    """
    usage example {{ your_dict|get_value_from_dict:your_key }}
    """
    if key:
        return dict_data.get(key)



from urllib.parse import urlencode
from collections import OrderedDict

@register.simple_tag
def url_replace(request, field, value, direction=''):
    dict_ = request.GET.copy()

    if field == 'order_by' and field in dict_.keys():
      if dict_[field].startswith('-') and dict_[field].lstrip('-') == value:
        dict_[field] = value
      elif dict_[field].lstrip('-') == value:
        dict_[field] = "-" + value
      else:
        dict_[field] = direction + value
    else:
      dict_[field] = direction + value

    return urlencode(OrderedDict(sorted(dict_.items())))