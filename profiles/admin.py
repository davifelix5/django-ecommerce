from django.contrib import admin
from . import models


class AddressInline(admin.StackedInline):
    model = models.Address
    extra = 1


class ProfileAdmin(admin.ModelAdmin):
    model = models.UserProfile
    inlines = [
        AddressInline
    ]


admin.site.register(models.UserProfile, ProfileAdmin)
admin.site.register(models.Address)

# Register your models here.
