from django.contrib import admin
from django.contrib.auth.models import User
from . import models


class AddressInline(admin.StackedInline):
    model = models.Address
    extra = 1


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'birth', 'cpf']
    model = models.UserProfile
    inlines = [
        AddressInline
    ]


class AddressAdmin(admin.ModelAdmin):
    model = models.Address
    list_display = ['user', 'cep', 'city', 'federation']


admin.site.register(models.UserProfile, ProfileAdmin)
admin.site.register(models.Address, AddressAdmin)

# Register your models here.
