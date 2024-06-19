from rest_framework import serializers
from .models import Commentaire

class CommentaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentaire
        fields = ["titre", "commentaire", "date"]