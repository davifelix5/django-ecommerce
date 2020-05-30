from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse


class Login(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Login')


class Logout(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Logout')


class SignIn(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Sign In')


class Update(View):
    def get(self, *args, **kwargs):
        return HttpResponse('update')
