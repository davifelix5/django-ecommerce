import locale
from django import template

locale.setlocale(locale.LC_ALL, '')
register = template.Library()


@register.filter(name='money')
def money(value):
    return locale.currency(value, grouping=True)
