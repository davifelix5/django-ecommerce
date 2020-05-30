import locale
import re

locale.setlocale(locale.LC_MONETARY, 'pt-br')


def format_value(value):
    return locale.currency(value, grouping=True)


def format_value_back(value):
    return float(re.sub(r'[^0-9.]', '', locale.delocalize(value)))
