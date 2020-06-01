from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from . import models
from . import forms


class SignIn(View):

    template_name = 'profiles/signin.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.context = {
            'userform': forms.UserFormCreate(self.request.POST or None),
            'profileform': forms.ProfileForm(self.request.POST or None),
            'addressform': forms.AddressForm(self.request.POST or None),
        }

        self.userform = self.context.get('userform')
        self.profileform = self.context.get('profileform')
        self.addressform = self.context.get('addressform')

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):

        if self.request.user:
            messages.add_message(
                self.request,
                messages.WARNING,
                'Você já está logado(a)!'
            )
            return redirect('profile:signin')

        if not self.userform.is_valid() or \
            not self.profileform.is_valid() or \
                not self.addressform.is_valid():

            messages.add_message(
                self.request,
                messages.WARNING,
                'Atençã, corrija os erros abaixo!'
            )
            return render(self.request, self.template_name, self.context)

        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')

        user = self.userform.save(commit=False)
        user.set_password(password)  # Faz a encriotação
        user.save()

        user_profile = self.profileform.save(commit=False)
        user_profile.user = user
        user_profile.save()

        address = self.addressform.save(commit=False)
        address.user = user_profile
        address.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Usuário cadastrado com sucesso'
        )

        auth = authenticate(
            self.request,
            username=username,
            password=password,
        )

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Você foi atumaticamente logado(a) na sua conta'
        )

        if auth:
            login(self.request, user=user)

        return redirect('profile:signin')


class Update(View):

    # TODO Dar a opção de listar quan mais de um endereço
    # TODO Dar a opção de adicionar endereços

    template_name = 'profiles/update.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.user = get_object_or_404(
            User, username=self.request.user.username)
        self.profile = get_object_or_404(models.UserProfile, user=self.user)
        self.address = get_object_or_404(models.Address, user=self.profile)

        self.context = {
            'userform': forms.UserFormUpdate(
                self.request.POST or None,
                instance=self.request.user
            ),
            'profileform': forms.ProfileForm(
                self.request.POST or None,
                instance=self.profile
            ),
            'addressform': forms.AddressForm(
                self.request.POST or None,
                instance=self.address
            ),
        }

        self.userform = self.context.get('userform')
        self.profileform = self.context.get('profileform')
        self.addressform = self.context.get('addressform')

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        # TODO fazer a funionalidade de mudar dados do usuário
        if not self.userform.is_valid() or \
            not self.profileform.is_valid() or \
                not self.addressform.is_valid():

            print('Ficou inválido')
            return redirect('profile:update')

        password = self.userform.cleaned_data.get('password', '')

        self.user.first_name = self.userform.cleaned_data.get('first_name')
        self.user.last_name = self.userform.cleaned_data.get('last_name')
        self.user.email = self.userform.cleaned_data.get('email')
        if password:
            self.user.set_password(password)  # Faz a encriotação
            messages.add_message(
                self.request,
                messages.INFO,
                'Sua senha foi alterada. Logue novamente'
            )
        self.user.save()

        if not self.profile:
            self.profileform.cleaned_data['user'] = self.user
            profile = models.UserProfile(**self.profileform.cleaned_data)
            profile.save()
        else:
            self.profile = self.profileform.save(commit=False)
            self.profile.user = self.user
            self.profile.save()

            self.address = self.addressform.save(commit=False)
            self.address.user = self.profile
            self.address.save()

        

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Usuário mudado com sucesso'
        )

        return redirect('profile:update')


class Login(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Login')


class Logout(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Logout')
