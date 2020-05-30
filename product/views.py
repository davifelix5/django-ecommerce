from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View


class ListProducts(ListView):
    pass


class ProductsDetails(View):
    pass


class Cart(View):
    pass


class AddToCart(View):
    pass


class RemoveFromCart(View):
    pass


class Finish(View):
    pass
