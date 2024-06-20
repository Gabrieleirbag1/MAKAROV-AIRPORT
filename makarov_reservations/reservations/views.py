from django.shortcuts import render
from .models import Reservations
from .serializer import InfoReservationsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.forms.models import model_to_dict

# Create your views here.
def index(request):
    return HttpResponseRedirect('/infos/')

def bool_convert(value):
    if value == 'True':
        return True
    return False

class ReservationsListApiView(APIView):

    def get(self, request):        
        vol_ref = request.query_params.get('vol_ref')
        if vol_ref is not None:
            reservation = Reservations.objects.filter(vol_ref=vol_ref).first()
            if reservation:
                reservation_dict = model_to_dict(reservation)
                return Response(reservation_dict, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No reservation found for this vol_ref'}, status=status.HTTP_404_NOT_FOUND)
        else:
            infos_volref= Reservations.objects.all()
            serializer = InfoReservationsSerializer(infos_volref, many=True)
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

        serializer = InfoReservationsSerializer(inforeservations)
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
            'vol_ref': request.data.get('vol_ref') or inforeservations.vol_ref,
            'user_ref': request.data.get('user_ref') or inforeservations.user_ref,
            'demande': bool_convert(request.data.get('demande')) if request.data.get('demande') is not None else inforeservations.demande,
            'annulation': bool_convert(request.data.get('annulation')) if request.data.get('annulation') is not None else inforeservations.annulation,
        }

        serializer = InfoReservationsSerializer(instance=inforeservations, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        print(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)