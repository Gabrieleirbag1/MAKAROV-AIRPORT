from .models import Vol
from .serializer import InfoVolSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests, time, random
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from datetime import datetime

# Create your views here.
def index(request):
    return HttpResponseRedirect('infos/')

class VolListApiView(APIView):

    def get(self, request):
        numvol = request.query_params.get('numvol')
        if numvol is not None:
            infosvols= Vol.objects.filter(numvol=numvol)
        else:
            infosvols= Vol.objects.all()

        serializer = InfoVolSerializer(infosvols, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        now_int = random.randint(0, 9999999)
        data = {
            'numvol': now_int,
            'aeroport_depart_ref': request.data.get('aeroport_depart_ref'),
            'aeroport_arrivee_ref': request.data.get('aeroport_arrivee_ref'),
            'date_depart': request.data.get('date_depart'),
            'date_arrivee': request.data.get('date_arrivee'),
            'heure_depart': request.data.get('heure_depart'),
            'heure_arrivee': request.data.get('heure_arrivee'),
            'prix': request.data.get('prix'),
            'type': request.data.get('type'),
            'avion_ref': request.data.get('avion_ref'),
        }

        serializer = InfoVolSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VolDetailApiView(APIView):

    def get(self, request, id, *args, **kwargs):
        vols= Vol.objects.get(id=id)
        if not vols:
            return Response({"response": f"Vol with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = InfoVolSerializer(vols)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, id, *args, **kwargs):
        vols= Vol.objects.get(id=id)
        if not vols:
            return Response({"response": f"Vol with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        response = requests.get(f"http://172.21.0.3:8003/reservations/infos/")
        response_data = response.json()
        for reservation in response_data:
            if reservation['vol_ref'] == vols.numvol:
                requests.delete(f"http://172.21.0.3:8003/reservations/infos/{reservation['id']}/")

        vols.delete()
        return Response({"response": f"Vol with id #{id} deleted successfully"}, status=status.HTTP_200_OK)
    
    def put(self, request, id, *args, **kwargs):
        vols= Vol.objects.get(id=id)
        if not vols:
            return Response({"response": f"Vol with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            'aeroport_depart_ref': request.data.get('aeroport_depart_ref') or vols.aeroport_depart_ref,
            'aeroport_arrivee_ref': request.data.get('aeroport_arrivee_ref') or vols.aeroport_arrivee_ref,
            'date_depart': request.data.get('date_depart') or vols.date_depart,
            'date_arrivee': request.data.get('date_arrivee') or vols.date_arrivee,
            'heure_depart': request.data.get('heure_depart') or vols.heure_depart,
            'heure_arrivee': request.data.get('heure_arrivee') or vols.heure_arrivee,
            'prix': request.data.get('prix') or vols.prix,
            'type': request.data.get('type') or vols.type,
            'avion_ref': request.data.get('avion_ref') or vols.avion_ref,
        }
        serializer = InfoVolSerializer(instance=vols, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)