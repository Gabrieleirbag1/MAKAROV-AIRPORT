from django.db import models

# Create your models here.
class UserProfile(models.Model):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
class Banque(models.Model):
    username = models.CharField(max_length=100, unique=True)
    argent = models.IntegerField(default=0)
    rib = models.CharField(max_length=10)

    def __str__(self):
        return self.rib
    
