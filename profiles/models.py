from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from utils.validate_cpf import validate_cpf
import re


class UserProfile(models.Model):

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Usuário")
    birth = models.DateField(verbose_name="Data de nascimento")
    cpf = models.CharField(max_length=11, verbose_name="CPF")

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def clean(self):
        error_messages = {}

        if not validate_cpf(self.cpf):
            error_messages['cpf'] = 'Digite um CPF válido'

        if error_messages:
            raise ValidationError(error_messages)


class Address(models.Model):

    FEDERATION_CHOICES = (
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    )

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    street = models.CharField(max_length=50, verbose_name="Rua")
    number = models.CharField(max_length=5, verbose_name="Número")
    complement = models.CharField(max_length=30, verbose_name="Complemento")
    neighbourhood = models.CharField(max_length=30, verbose_name="Bairro")
    cep = models.CharField(max_length=8, verbose_name="CEP")
    city = models.CharField(max_length=30, verbose_name="Cidade")
    federation = models.CharField(
        max_length=2, default="SP", choices=FEDERATION_CHOICES, verbose_name="Estado")

    def clean(self):
        error_messages = {}

        if not re.fullmatch(r'^[0-9]{8}$', self.cep):
            error_messages['cep'] = 'Digite um CEP válido!'

        if error_messages:
            raise ValidationError(error_messages)

    def __str__(self):
        return f'Endereço {self.pk}'
