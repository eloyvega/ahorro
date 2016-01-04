from django.conf import settings
from django.db import models


# Create your models here.
class Semana(models.Model):
    numero = models.IntegerField()
    cantidad = models.IntegerField(blank=True, null=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return 'Semana %s de %s' % (self.numero, self.usuario)
