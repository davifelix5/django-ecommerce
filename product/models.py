from django.db import models
from utils.resize_img import resize_img
from utils.format_money import format_value
from utils.format_money import format_value_back
from django.forms import ValidationError
from django.utils.text import slugify


class Product(models.Model):

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    TYPE_CHOICES = [
        ('V', 'Variável'),
        ('S', 'Simples')
    ]
    name = models.CharField(max_length=100, null=False,
                            blank=False, verbose_name='Nome do produto')
    short_desc = models.TextField(
        max_length=255, null=False, blank=False, verbose_name='Curta descrição')
    long_desc = models.TextField(
        null=True, blank=True, verbose_name='Descrição longa')
    image = models.ImageField(
        upload_to='produto_imagens/%Y/%m/', blank=True, null=True,
        verbose_name='Imagem do produto'
    )
    slug = models.SlugField(unique=True, verbose_name='Identificação para o produto',
                            blank=True, help_text="Pode ser gerado automaticamente",
                            max_length=255)
    price_display = models.FloatField(verbose_name='Preço padrão')
    price_promo = models.FloatField(
        default=0, verbose_name='Preço promocional', blank=True)
    prod_type = models.CharField(
        max_length=1, choices=TYPE_CHOICES, verbose_name='Tipo de produto', default="V")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = f'{slugify(self.name)}-{self.pk}'
        super().save(*args, **kwargs)
        print(self.slug)
        if self.image:
            resize_img(self.image)

    def price(self):
        return format_value(self.price_display)
    price.short_description = 'Preço padrão'

    def promo_price(self):
        return format_value(self.price_promo)
    promo_price.short_description = 'Preço promocional'

    def __str__(self):
        return self.name


class Variation(models.Model):

    class Meta:
        verbose_name = "Variação"
        verbose_name_plural = "Variações"

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Produto relacionado")
    name = models.CharField(max_length=80, blank=True,
                            null=True, verbose_name="Nome da variação")
    price = models.FloatField(verbose_name="Preço padrão")
    price_promo = models.FloatField(
        verbose_name="Produto promocional", blank=True, default=None, null=True)
    stock = models.PositiveIntegerField(
        default=1, verbose_name="Quantidade em estoque")

    def __str__(self):
        return self.name or self.product.name
