from django.db import models

# Create your models here.
class Aeroports(models.Model):
    nom = models.CharField(max_length=100)
    code_pays = models.CharField(max_length=3)
    fuseau = models.CharField(max_length=6)

    def __str__(self):
        return self.nom
    
class Staff(models.Model):
    user_ref = models.CharField(unique=True, max_length=100)
    aeroport_ref = models.ForeignKey(Aeroports, on_delete=models.CASCADE, related_name='nom_aeroport')
    level = models.IntegerField()

    def __str__(self):
        return f'{self.user_ref} -> {self.aeroport_ref}'

class Avions(models.Model):
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    places = models.IntegerField()
    image = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f'{self.marque} {self.modele}'

# Create your models here.
