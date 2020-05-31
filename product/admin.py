from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Product, Variation


class VariationInLine(admin.TabularInline):
    model = Variation
    extra = 1


class ProductAdmin(SummernoteModelAdmin):
    summernote_fields = ['long_desc']
    list_display = ['id', 'name', 'price', 'promo_price']
    list_display_links = ['id', 'name', 'price', 'promo_price']
    inlines = [
        VariationInLine
    ]


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation)

# Register your models here.
