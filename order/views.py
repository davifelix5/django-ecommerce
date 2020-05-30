from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse


class Pay(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Pay')


class Finish(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finish')


class Details(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Details')
