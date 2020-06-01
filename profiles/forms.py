from django import forms
from django.contrib.auth.models import User
from django.contrib import messages
from django.forms import ValidationError
from . import models


class ProfileForm(forms.ModelForm):

    class Meta:
        model = models.UserProfile
        fields = '__all__'
        exclude = ['user']


class UserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages = {}

    def clean(self):
        raw_data = self.data
        clean_data = self.cleaned_data

        form_user = clean_data.get('username')
        form_email = clean_data.get('email')
        form_password = clean_data.get('password', '')
        form_password2 = clean_data.get('password2', '')

        self.template_method(
            form_user,
            form_email,
            form_password,
            form_password2
        )

        if self.error_messages:
            raise ValidationError(self.error_messages)

    def validate_username(self, username):
        user_with_username = User.objects.filter(username=username).first()
        if user_with_username:
            self.error_messages['username'] = 'Esse usuário já existe'

    def validate_email(self, email):
        user_with_email = User.objects.filter(email=email).first()
        if user_with_email:
            self.error_messages['email'] = 'Esse email já foi cadastrado'

    def validate_password(self, pass1, pass2):
        if not pass1 or not pass2:
            return
        if pass1 != pass2:
            self.error_messages['password'] = 'Senhas informandas não coincidem'
        else:
            if len(pass1) < 6:
                self.error_messages['password'] = 'Senha deve pelo mesno 6 caracteres'

    def template_method(self, user, email, password1, password2):
        pass


class UserFormCreate(UserForm):

    username = forms.CharField(required=True, label='Usuário')
    first_name = forms.CharField(required=True, label='Primeiro nome')
    last_name = forms.CharField(required=True, label='Sobrenome')
    email = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'email', 'username', 'password', ]

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Senha'
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Repetição da senha'
    )

    def template_method(self, user, email, password1, password2):
        self.validate_username(user)
        self.validate_email(email)
        self.validate_password(password1, password2)


class UserFormUpdate(UserForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', ]
        exclude = ['username']

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha',
        help_text='Deixe vazio para não alterar sua senha'
    )

    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Repetição da senha',
        help_text='Deixe vazio para não alterar sua senha'
    )

    def template_method(self, user, email, password1, password2):
        self.validate_password(password1, password2)


class AddressForm(forms.ModelForm):

    class Meta:
        model = models.Address
        fields = '__all__'
        exclude = ['user']
