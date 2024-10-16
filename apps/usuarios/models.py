from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ESTADO_CHOICES = (
        ('activo', 'Activo'),
        ('bloqueado', 'Bloqueado'),
    )
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')

class Noticia(models.Model):
    # Otros campos
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, default=1)
