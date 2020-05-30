from django.contrib import admin
from . import models


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    model = models.Order
    inlines = [
        OrderItemInline
    ]


admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem)

# Register your models here.
