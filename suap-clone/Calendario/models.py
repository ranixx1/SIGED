from django.db import models
from django.utils import timezone

class Evento(models.Model):
    titulo =models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    data_evento= models.DateField()
    cor = models.CharField(max_length=20, default='#7a9a5a', help_text="Cor em formato hexadecimal, ex: #7a9a5a")


    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['data_evento']


