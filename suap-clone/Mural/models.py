from django.db import models

# Create your models here.
class Card(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()

    def __str__(self):
        return self.titulo
    
    class Meta:
        db_table = 'App_card'