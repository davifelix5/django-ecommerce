from django.shortcuts import render, redirect, reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.contrib import messages
from . import models
from . import product_services
from django.http import HttpResponse
from pprint import pprint


class ListProducts(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 10
    paginate_orphans = 3

    def get_queryset(self):
        return product_services.get_products()


class ProductsDetails(DetailView):
    model = models.Product
    template_name = 'product/details.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['variations'] = product_services.get_variations(
            self.get_object())
        context['selected_variation'] = context['variations'][0]
        return context


class Cart(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'product/cart.html')


class AddToCart(View):
    """
        Se o formulário estivesse usando o método POST, deveria ser definido o
    método post

    COOKIES: arquivos armazenado dados úteis no computador do cliente
    SESSÃO: conta com dados mais sensíveis, que são salvos no server side
        Para entrar nela, é salvo um cookie no server apenas com a session key
    """

    def get(self, *args, **kwargs):
        """
        Encapsular função que recebe o variation ID e retorna para o carrinho
        """
        previous_url = self.request.META.get('HTTP_REFERER')
        variation_id = self.request.GET.get('vid')

        if not previous_url:
            messages.add_message(
                self.request,
                messages.ERROR,
                'Erro! Adicione o produto novamente ao carrinho'
            )
            return redirect('product:list')

        if not variation_id:
            messages.add_message(
                self.request,
                messages.ERROR,
                'Esse produto não exite'
            )
            return redirect(previous_url)

        cart = product_services.add_to_cart(self.request, variation_id)

        messages.add_message(self.request, messages.SUCCESS,
                             'Produto adicionado ao carrinho!')

        pprint(cart)
        return redirect(previous_url)


class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        previous_url = self.request.META.get('HTTP_REFERER')
        variation_id = self.request.GET.get('vid')

        if not previous_url:
            messages.add_message(
                self.request,
                messages.ERROR,
                'Erro! Tente remover novamente'
            )
            return redirect('product:list')

        if not variation_id:
            messages.add_message(
                self.request,
                messages.ERROR,
                'Esse produto não exite'
            )
            return redirect(previous_url)

        if not self.request.session['cart']:
            messages.add_message(
                self.request,
                messages.ERROR,
                'Erro! Não há um carrinho registrado nessa sessão'
            )
            return redirect(previous_url)

        if not variation_id in self.request.session['cart']:
            messages.add_message(
                self.request,
                messages.ERROR,
                'Esse produto não está em seu carrinho'
            )
            return redirect(previous_url)

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Produto removido com sucesso'
        )

        del self.request.session['cart'][variation_id]
        self.request.session.save()
        return redirect(previous_url)


class OrderInfo(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Final do pedido')