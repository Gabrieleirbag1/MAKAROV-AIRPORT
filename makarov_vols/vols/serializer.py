
from rest_framework import serializers
from .models import Vol

class InfoVolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vol
        fields = ["id",
                  "numvol",
                  "aeroport_depart_ref", 
                  "aeroport_arrivee_ref", 
                  "date_depart", 
                  "date_arrivee", 
                  "heure_depart", 
                  "heure_arrivee", 
                  "prix",
                  "type",
                  "avion_ref"]