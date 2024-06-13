from django.shortcuts import render
from .models import Reservations
from .serializer import InfoReservationsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def index(request):
    return HttpResponseRedirect('/infos/')

def bool_convert(value):
    if value == 'True':
        return True
    return False

class ReservationsListApiView(APIView):

    def get(self, request):
        infosreservations= Reservations.objects.all()
        serializer = InfoReservationsSerializer(infosreservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request, *args, **kwargs):
        data = {
            'vol_ref': request.data.get('vol_ref'),
            'user_ref': request.data.get('user_ref'),
            'demande': bool_convert(request.data.get('demande')),
            'annulation': bool_convert(request.data.get('annulation')),
        }

        serializer = InfoReservationsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ReservationsDetailApiView(APIView):

    def get(self, request, id, *args, **kwargs):
        inforeservations= Reservations.objects.get(id=id)
        if not inforeservations:
            return Response({"response": f"InfosAlbum with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = Reservations(inforeservations)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def delete(self, request, id, *args, **kwargs):
        inforeservations= Reservations.objects.get(id=id)
        if not inforeservations:
            return Response({"response": f"InfosAlbum with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        inforeservations.delete()
        return Response({"response": f"InfosAlbum with id #{id} deleted successfully"}, status=status.HTTP_200_OK)
    
    def put(self, request, id, *args, **kwargs):
        inforeservations= Reservations.objects.get(id=id)
        if not inforeservations:
            return Response({"response": f"InfosAlbum with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            'vol_ref': request.data.get('vol_ref'),
            'user_ref': request.data.get('user_ref'),
            'demande': bool_convert(request.data.get('demande')),
            'annulation': bool_convert(request.data.get('annulation')),
        }

        serializer = Reservations(instance=inforeservations, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)