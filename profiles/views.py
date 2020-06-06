from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from copy import deepcopy
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

        if self.request.user.is_authenticated:
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

        return redirect('procuct:list')


class Update(View):
    # TODO Corrigir métodos adicionando o get_context_data()

    template_name = 'profiles/update.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.user = get_object_or_404(
            User, username=self.request.user.username)
        self.profile = get_object_or_404(models.UserProfile, user=self.user)
        self.addresses = self.user.userprofile.address_set.all()

        self.context = {
            'userform': forms.UserFormUpdate(
                self.request.POST or None,
                instance=self.request.user
            ),
            'profileform': forms.ProfileForm(
                self.request.POST or None,
                instance=self.profile
            ),
            'main_address': self.addresses.first(),
            'other_addresses': self.addresses[1:]
        }

        self.userform = self.context.get('userform')
        self.profileform = self.context.get('profileform')

        self.redirect = 'profile:update'

    def get(self, *args, **kwargs):
        edit_id = self.request.GET.get('changeAddress')
        if edit_id:
            return HttpResponseRedirect(reverse('profile:edit_address', kwargs={'pk': int(edit_id)}))

        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        print('posting')

        if not self.userform.is_valid() or \
                not self.profileform.is_valid():

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
            # Caso a senha tenha sido alterada, precisa logar denovo
            self.redirect = 'product:list'
        self.user.save()

        if not self.profile:
            self.profileform.cleaned_data['user'] = self.user
            profile = models.UserProfile(**self.profileform.cleaned_data)
            profile.save()
        else:
            self.profile = self.profileform.save(commit=False)
            self.profile.user = self.user
            self.profile.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Usuário mudado com sucesso'
        )

        return redirect(self.redirect)


class Login(View):

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.login_form = forms.LoginForm(self.request.POST or None)
        self.context = {'form_login': self.login_form}

    def get(self, *args, **kwargs):
        return render(self.request, 'profiles/login.html', self.context)

    def post(self, *args, **kwargs):
        if not self.login_form.is_valid():
            messages.warning(self.request, 'Atenção! Corrija os erros abaixo.')
            return render(self.request, 'profiles/login.html', self.context)

        username = self.login_form.cleaned_data.get('username')
        password = self.login_form.cleaned_data.get('password')
        user = authenticate(self.request, username=username,
                            password=password)

        if user:
            login(self.request, user)
            if self.request.session.get('next_page'):
                messages.success(
                    self.request, 'Logado com sucesso. Continua sua compra!')
                del self.request.session['next_page']
                return redirect('product:info')

            messages.success(
                self.request, 'Logado com sucesso')
            return redirect('product:list')

        messages.error(self.request, 'Dados incorretos! Tente novamente.')

        next_page = self.request.session.get('next_page', 'profile:login')
        return redirect(next_page)


class NewAddress(View):

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.context = {
            'address_form': forms.AddressForm(self.request.POST or None)
        }
        self.address_form = self.context.get('address_form')

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('profile:login')
        return render(self.request, 'profiles/new_address.html', self.context)

    def post(self, *args, **kwargs):
        if not self.address_form.is_valid():
            messages.warning(self.request, 'Preencha os campos corretamente')
            return render(self.request, 'profiles/new_address.html', self.context)

        address = self.address_form.save(commit=False)
        address.user = self.request.user.userprofile
        address.save()
        messages.success(self.request, 'Endereço adicionado')
        return redirect('profile:update')


@login_required
def edit_address(request, pk):
    specific_address = models.Address.objects.filter(id=pk).first()
    context = {'address_form': forms.AddressForm(
        request.POST or None,
        instance=specific_address
    )}
    if not request.user.userprofile == specific_address.user:
        raise PermissionDenied()

    if request.method == 'POST':
        specific_address = context['address_form'].save(commit=False)
        specific_address.user = request.user.userprofile
        specific_address.save()
        messages.success(request, 'Endereço alterado com sucesso')
        return redirect('profile:update')

    return render(request, 'profiles/new_address.html', context)


class Logout(View):

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('profile:login')

        cart = self.request.session.get('cart', '')
        copy_cart = deepcopy(cart)
        logout(self.request)
        self.request.session['cart'] = copy_cart
        return redirect('profile:login')
