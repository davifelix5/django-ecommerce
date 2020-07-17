from product import models
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Window, Q, Min


def get_variations(product_obj):
    return models.Variation.objects.filter(
        product=product_obj
    )


def get_variation(pk):
    return get_object_or_404(models.Variation, id=pk)


def get_products():
    # TODO transformar isso pra ORM
    return models.Variation.objects.raw('''
        SELECT product.*, variation.id AS v_id,
        variation.price AS v_price,
        variation.price_promo AS v_price_promo
        FROM product_product AS product
        JOIN product_variation AS variation
        ON product.id = variation.product_id
        WHERE variation.price = (
            SELECT Min(v.price)
            FROM product_variation AS v
            JOIN product_product AS p
            ON p.id = v.product_id
            WHERE p.id = product.id
        )
        GROUP BY product.id
        ORDER BY product.id DESC;
    ''')


def check_stock(pk):
    return (get_variation(pk).stock > 1)


def add_to_cart(request, pk):
    previous_url = request.META.get('HTTP_REFERER')

    variation = get_variation(pk)
    product = variation.product
    product_name = variation.product.name
    variation_name = variation.name
    price = variation.price
    promo_price = variation.price_promo
    slug = product.slug
    image = product.image.name if product.image else ''

    if variation.stock < 1:
        messages.warning(
            request,
            f'Desculpe, não temos mais estoque para "{variation.product.name}'
            f' {variation.name}"!'
        )
        return False

    if not request.session.get('cart'):
        request.session['cart'] = {}
        request.session.save()

    cart = request.session['cart']

    if pk in cart:
        amount = cart[pk]['amount']
        amount += 1
        cart[pk]['subtotal'] = price * amount
        cart[pk]['promo_subtotal'] = promo_price * amount
        cart[pk]['amount'] = amount
        request.session.save()

    else:
        cart[pk] = {
            'pk': pk,
            'product_id': product.id,
            'product_name': product_name,
            'variation_name': variation_name,
            'variation_id': pk,
            'price': price,
            'promo_price': promo_price,
            'subtotal': price,
            'promo_subtotal': promo_price,
            'slug': slug,
            'image': image,
            'amount': 1
        }

    variation.stock -= 1
    variation.save()
    request.session.save()
    return True


def remove_from_cart(request, variation_id, amount=0):
    variation = get_variation(variation_id)

    if amount:
        amount = int(amount)
        cart = request.session['cart'][variation_id]

        cart['promo_subtotal'] -= cart['promo_price'] * amount
        cart['subtotal'] -= cart['price'] * amount

        cart['amount'] -= amount

        if cart['amount'] == 0:
            del request.session['cart'][variation_id]

        variation.stock += amount
        variation.save()
        request.session.save()
        return

    variation.stock += request.session['cart'][variation_id]['amount']
    del request.session['cart'][variation_id]
    variation.save()
    request.session.save()
