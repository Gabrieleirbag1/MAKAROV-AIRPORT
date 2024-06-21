from django.shortcuts import render
from .models import Aeroports, Staff, Avions
from .serializer import InfoAeroportsSerializer, InfoStaffSerializer, InfoAvionsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def index(request):
    return HttpResponseRedirect('/infos/')

class AvionsListApiView(APIView):

    def get(self, request):
        modele = request.query_params.get('modele')
        if modele is not None:
            infosavions= Avions.objects.filter(modele=modele)
            print(infosavions)
        else:
            infosavions= Avions.objects.all()
        serializer = InfoAvionsSerializer(infosavions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request, *args, **kwargs):
        data = {
            'marque': request.data.get('marque'),
            'modele': request.data.get('modele'),
            'places': request.data.get('places'),
            'image': request.data.get('image'),
        }

        serializer = InfoAvionsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AvionsDetailApiView(APIView):

    def get(self, request, id, *args, **kwargs):
        infoavion= Avions.objects.get(id=id)
        if not infoavion:
            return Response({"response": f"InfosAlbum with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = Avions(infoavion)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def delete(self, request, id, *args, **kwargs):
        infoavion= Avions.objects.get(id=id)
        if not infoavion:
            return Response({"response": f"InfosAlbum with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        infoavion.delete()
        return Response({"response": f"InfosAlbum with id #{id} deleted successfully"}, status=status.HTTP_200_OK)
    
    def put(self, request, id, *args, **kwargs):
        infoavion= Avions.objects.get(id=id)
        if not infoavion:
            return Response({"response": f"InfosAlbum with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            'marque': request.data.get('marque'),
            'modele': request.data.get('modele'),
            'places': request.data.get('places'),
            'image': request.data.get('image'),
        }

        serializer = Avions(instance=infoavion, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#####################################################################
    
class StaffListApiView(APIView):

    def get(self, request):
        infosstaff= Staff.objects.all()
        serializer = InfoStaffSerializer(infosstaff, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request, *args, **kwargs):
        data = {
            'user_ref': request.data.get('user_ref'),
            'aeroport_ref': request.data.get('aeroport_ref'),
            'level': request.data.get('level'),
        }

        serializer = InfoStaffSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StaffDetailApiView(APIView):

    def get(self, request, id, *args, **kwargs):
        infosstaff= Staff.objects.get(id=id)
        if not infosstaff:
            return Response({"response": f"InfosStaff with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = InfoStaffSerializer(infosstaff)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def delete(self, request, id, *args, **kwargs):
        infosstaff= Staff.objects.get(id=id)
        if not infosstaff:
            return Response({"response": f"InfosStaff with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        infosstaff.delete()
        return Response({"response": f"InfosStaff with id #{id} deleted successfully"}, status=status.HTTP_200_OK)
    
    def put(self, request, id, *args, **kwargs):
        infosstaff= Staff.objects.get(id=id)
        if not infosstaff:
            return Response({"response": f"InfosStaff with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            'user_ref': request.data.get('user_ref'),
            'aeroport_ref': request.data.get('aeroport_ref'),
            'level': request.data.get('level'),
        }

        serializer = InfoStaffSerializer(instance=infosstaff, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

###############################################################

class AeroportsListApiView(APIView):
    
    def get(self, request):
        infosaeroport= Aeroports.objects.all()
        serializer = InfoAeroportsSerializer(infosaeroport, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request, *args, **kwargs):
        data = {
            'nom': request.data.get('nom'),
            'code_pays': request.data.get('code_pays'),
            'fuseau': request.data.get('fuseau'),
        }

        serializer = InfoAeroportsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class AeroportsDetailApiView(APIView):

    def get(self, request, id, *args, **kwargs):
        infosaeroport= Aeroports.objects.get(id=id)
        if not infosaeroport:
            return Response({"response": f"InfosAeroport with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = InfoAeroportsSerializer(infosaeroport)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def delete(self, request, id, *args, **kwargs):
        infosaeroport= Aeroports.objects.get(id=id)
        if not infosaeroport:
            return Response({"response": f"InfosAeroport with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        infosaeroport.delete()
        return Response({"response": f"InfosAeroport with id #{id} deleted successfully"}, status=status.HTTP_200_OK)
    
    def put(self, request, id, *args, **kwargs):
        infosaeroport= Aeroports.objects.get(id=id)
        if not infosaeroport:
            return Response({"response": f"InfosAeroport with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            'nom': request.data.get('nom'),
            'code_pays': request.data.get('code_pays'),
            'fuseau': request.data.get('fuseau'),
        }

        serializer = InfoAeroportsSerializer(instance=infosaeroport, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
