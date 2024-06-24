from django.db import models

# Create your models here.
class Reservations(models.Model):
    vol_ref = models.IntegerField()
    user_ref = models.CharField(max_length=100)
    demande = models.BooleanField(default=False)
    annulation = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Reservation {self.id} pour le vol {self.vol_ref} par {self.user_ref}"