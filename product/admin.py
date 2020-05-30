from django.contrib import admin
from .models import Product, Variation


class VariationInLine(admin.TabularInline):
    model = Variation
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'promo_price']
    list_display_links = ['id', 'name', 'price', 'promo_price']
    inlines = [
        VariationInLine
    ]


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation)

# Register your models here.
