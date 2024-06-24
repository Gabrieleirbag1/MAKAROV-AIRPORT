from rest_framework import serializers
from .models import Reservations

class InfoReservationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservations
        fields = ["id", "vol_ref", "user_ref", "demande", "annulation"]