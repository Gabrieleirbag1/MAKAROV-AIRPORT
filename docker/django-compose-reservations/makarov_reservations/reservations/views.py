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
    """index() : redirige vers la page d'informations de vol
    
    Args:
        request (HttpRequest): requête HTTP"""
    return HttpResponseRedirect('/infos/')

def bool_convert(value):
    """bool_convert() : convertit une chaine de caractère en booléen
    
    Args:
        value (str): chaine de caractère à convertir"""
    if value == 'True':
        return True
    return False

class ReservationsListApiView(APIView):

    def get(self, request):        
        """get() : get tous les enregistrements d'informations de vol ou un enregistrement d'informations de vol par vol_ref
        
        Args:
            request (HttpRequest): requête HTTP"""
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
        """post() : crée un nouvel enregistrement d'informations de vol"""
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
    """ReservationsDetailApiView() : APIView pour les informations de vol"""
    def get(self, request, id, *args, **kwargs):
        """get() : get les informations d'un vol
        
        Args:
            request (HttpRequest): requête HTTP
            id (int): id de l'information de vol à récupérer"""
        inforeservations= Reservations.objects.get(id=id)
        if not inforeservations:
            return Response({"response": f"InfosAlbum with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = InfoReservationsSerializer(inforeservations)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id, *args, **kwargs):
        """delete() : supprime les informations d'un vol
        
        Args:
            request (HttpRequest): requête HTTP
            id (int): id de l'information de vol à supprimer"""
        inforeservations= Reservations.objects.get(id=id)
        if not inforeservations:
            return Response({"response": f"InfosAlbum with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        inforeservations.delete()
        return Response({"response": f"InfosAlbum with id #{id} deleted successfully"}, status=status.HTTP_200_OK)
    
    def put(self, request, id, *args, **kwargs):
        """put() : update les informations d'un vol
        
        Args:
            request (HttpRequest): requête HTTP
            id (int): id de l'information de vol à mettre à jour"""
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
    
class UserVolsListApiView(APIView):
    """UserVolsListApiView() : APIView pour les vols d'un utilisateur"""
    def get(self, request):
        """get() : get tous les vols d'un utilisateur
        
        Args:
            request (HttpRequest): requête HTTP"""
        user_ref = request.query_params.get('user_ref')
        if user_ref is not None:
            infosvols= Reservations.objects.filter(user_ref=user_ref)
        else:
            infosvols= Reservations.objects.all()

        serializer = InfoReservationsSerializer(infosvols, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)