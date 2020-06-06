from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    STATUS = (
        ('A', 'Aprovado'),
        ('C', 'Criado'),
        ('R', 'Reprovado'),
        ('P', 'Pendente'),
        ('E', 'Enviado'),
        ('F', 'Finalizado'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=False, blank=False, verbose_name="Usuário")
    total_price = models.FloatField(verbose_name="Preço total do pedido")
    amount = models.PositiveIntegerField(
        verbose_name="Quantidade total de produtos")
    status = models.CharField(max_length=1, choices=STATUS, default='C',
                              verbose_name="Status do pedido")

    def __str__(self):
        # Pega a primary key
        return f'Pedido Nº{self.pk}'


class OrderItem(models.Model):
    """
        O produto não pode ser buscado novamente na base de dados, pois os
    dados desse produto podem ter siso alterados após a compra, o que também
    alteraria o pedido do cliente, o que não é um comportamente esperado
        Essa classe deve ser registrada no momento da compra
    """

    class Meta:
        verbose_name = "Item do pedido"
        verbose_name_plural = "Itens do pedido"

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name="Pedido relacionado")
    product_name = models.CharField(
        max_length=100, verbose_name="Nome do produto")
    product_id = models.PositiveIntegerField(verbose_name="ID do produto")
    variation_name = models.CharField(
        max_length=80, verbose_name="Nome da variação", blank=True, null=True)
    variation_id = models.PositiveIntegerField(verbose_name="ID da variação")
    total_price = models.FloatField(verbose_name="Preço total")
    total_promo_price = models.FloatField(
        verbose_name="Preço promocional total")
    amount = models.PositiveIntegerField(
        verbose_name="Quantidade total do produto")
    # O tamanho do caminho da imagem pode ser muito grande
    image_path = models.CharField(
        max_length=2000, verbose_name="Caminho da imagem do produto")

    def __str__(self):
        return f'Item do pedido Nº {self.order}'
