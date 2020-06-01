from product import models
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages


def get_variations(product_obj):
    return models.Variation.objects.filter(
        product=product_obj
    )


def get_variation(pk):
    return get_object_or_404(models.Variation, id=pk)


def get_products():
    return models.Product.objects.order_by('-id')


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
        messages.add_message(
            request,
            messages.WARNING,
            f'Desculpe, não temos mais estoque desse produto!'
        )

    if not request.session.get('cart'):
        request.session['cart'] = {}
        request.session.save()

    cart = request.session['cart']

    if pk in cart:
        amount = cart[pk]['amount']
        amount += 1

        if variation.stock < amount:
            messages.add_message(request, messages.WARNING,
                                 f'Estoque insuficiente para o produto "{product.name}"')

            return redirect(previous_url)

        cart[pk]['amount'] = amount
        cart[pk]['subtotal'] = price * amount
        cart[pk]['promo_subtotal'] = promo_price * amount

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

    request.session.save()
    return cart
