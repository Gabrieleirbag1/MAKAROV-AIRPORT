from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     argent = models.IntegerField(default=0)

#     def __str__(self):
#         return self.user.username

# class Aeroport(models.Model):
#     nom = models.CharField(max_length=100)
#     code_pays = models.CharField(max_length=3)
#     fuseau = models.CharField(max_length=6)

#     def __str__(self):
#         return self.nom
    
class Vol(models.Model):
    numvol = models.IntegerField()
    aeroport_depart_ref = models.IntegerField()
    aeroport_arrivee_ref = models.IntegerField()
    date_depart = models.DateField()
    date_arrivee = models.DateField()
    heure_depart = models.TimeField()
    heure_arrivee = models.TimeField()
    prix = models.IntegerField()
    type = models.CharField(max_length=100)
    avion_ref = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.aeroport_depart_ref} -> {self.aeroport_arrivee_ref}'