from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User


class Sala(models.Model):
    sala = models.CharField(max_length=50, blank=True, null=False)
    usuarios_permitidos = models.ManyToManyField(User, related_name='usuarios_permitidos')
    data_criada = models.DateField(default=timezone.now)


class Mensagem(models.Model):
    mensagem = models.TextField(blank=True, null=False)
    remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='remetente')
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='mensagens')

    