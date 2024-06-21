
from rest_framework import serializers
from .models import UserProfile, Banque

class InfoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "username", "first_name", "last_name", "email", "password", "is_superuser",]

class InfoBanqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banque
        fields = ["id", "username", "argent", "rib"]