from django.db import models
from datetime import date
from django.contrib .auth.models import User

# Create your models here.
"""
 nom
 image
 date
"""
class Todo(models.Model):
    nom = models.CharField(max_length=100, verbose_name="nom")
    image = models.ImageField(verbose_name="image", null=True, blank=True)
    statut = models.BooleanField(verbose_name="statut",)
    date = models.DateField(default=date.today, verbose_name="date")
    idUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="idUser")


    def __str__(self):
        return f"{self.nom} ({self.descprion})"
    
    class Meta:
        verbose_name = "Todo"
        verbose_name_plural = "Todos"
# Create your models here.