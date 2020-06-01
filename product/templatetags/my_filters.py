import locale
from django import template
from functools import reduce

locale.setlocale(locale.LC_ALL, '')
register = template.Library()


@register.filter(name='money')
def money(value):
    return locale.currency(value, grouping=True)


@register.filter(name='cart')
def cart(value):
    return reduce(lambda ac, item: ac + item['amount'], value.values(), 0)


@register.filter(name='get_total')
def get_total(value):

    def get_prices(ac, item):
        if item['promo_subtotal']:
            return ac + item['promo_subtotal']
        return ac + item['subtotal']

    return reduce(get_prices, value.values(), 0)
