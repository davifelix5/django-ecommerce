from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views import View
from django.contrib import messages
from product.product_services import check_stock
from django.http import HttpResponse
from .models import Order, OrderItem
import utils.cart as cart_utils
from copy import deepcopy


class SafetyMixin(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, 'Faça login primeiro!')
            self.request.session['next_page'] = 'order:finish'
            return redirect('profile:login')
        return super().dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(user=self.request.user)
        return queryset


class Details(SafetyMixin, DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'order/details.html'
    pk_url_kwarg = 'pk'


class List(SafetyMixin, ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'order/list.html'
    paginate_by = 5


class Pay(SafetyMixin, DetailView):
    template_name = 'order/pay.html'
    model = Order
    pk_url_kwarg = 'pk'
    context_object_name = 'order'


class Finish(View):
    template_name = 'order/pay.html'

    def get(self, *args, **kwargs):

        cart = self.request.session.get('cart')

        if not self.request.user.is_authenticated:
            messages.warning(self.request, 'Você precisa estar logado')
            return redirect('profile:login')

        if not cart:
            messages.warning(self.request, 'Seu carrinho está vazio!')
            return redirect('product:list')

        total_amount = cart_utils.cart_amount(cart)
        total_price = cart_utils.cart_total(cart)

        order = Order(
            user=self.request.user,
            total_price=total_price,
            amount=total_amount,
            status='C',
        )

        order.save()

        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    product_name=varitation['product_name'],
                    product_id=varitation['product_id'],
                    variation_name=varitation['variation_name'],
                    variation_id=varitation['variation_id'],
                    image_path=varitation['image'],
                    total_price=varitation['subtotal'],
                    total_promo_price=varitation['promo_subtotal'],
                    amount=varitation['amount'],
                ) for varitation in cart.values()
            ]
        )

        del self.request.session['cart']
        self.request.session.save()

        # Aqui redirecionaria para o serciço de pagar com uma mensagem
        messages.success(self.request, 'Pedido registrado com sucesso')
        return redirect(reverse('order:pay', kwargs={'pk': order.id}))
