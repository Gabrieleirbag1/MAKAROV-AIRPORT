from django.db import models

# Create your models here.
class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    is_superuser = models.BooleanField(default=False)
    argent = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username