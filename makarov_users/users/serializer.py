
from rest_framework import serializers
from .models import UserProfile

class InfoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["username", "email", "password", "is_superuser", "argent"]