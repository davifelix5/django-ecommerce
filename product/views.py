from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse
from . import models


class ListProducts(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 10
    paginate_orphans = 3

    def get_queryset(self):
        return self.model.objects.all().order_by('-id')


class ProductsDetails(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Details')


class Cart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Cart')


class AddToCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Add')


class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Remove')
