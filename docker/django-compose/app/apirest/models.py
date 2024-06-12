from django.db import models

# Create your models here.
class Commentaire(models.Model):
    titre = models.CharField(max_length=200)
    commentaire = models.TextField()
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.commentaire
    
    def __repr__(self) -> str:
        return self.titre, self.commentaire, self.date