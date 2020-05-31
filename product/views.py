from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
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


class ProductsDetails(DetailView):
    model = models.Product
    template_name = 'product/details.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['variations'] = models.Variation.objects.filter(
            product=self.get_object()
        ).select_related('product')
        context['selected_variation'] = context['variations'][0]
        return context


class Cart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Cart')


class AddToCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Add')


class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Remove')
