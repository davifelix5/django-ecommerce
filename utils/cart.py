from functools import reduce


def cart_amount(cart):
    return reduce(lambda ac, item: ac + item['amount'], cart.values(), 0)


def cart_total(cart):

    def get_prices(ac, item):
        if item['promo_subtotal']:
            return ac + item
        return item['subtotal']

    return reduce(get_prices, cart.values(), 0)
