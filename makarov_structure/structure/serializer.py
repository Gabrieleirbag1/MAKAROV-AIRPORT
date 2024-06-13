from rest_framework import serializers
from .models import Aeroports, Staff, Avions

class InfoAeroportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aeroports
        fields = ["nom", "code_pays", "fuseau"]

class InfoStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ["user_ref", "aeroport_ref", "level"]

class InfoAvionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avions
        fields = ["marque", "modele", "places", "image"]