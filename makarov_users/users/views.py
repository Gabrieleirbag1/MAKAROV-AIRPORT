from .models import UserProfile
from .serializer import InfoUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponseRedirect('infos/')

def bool_convert(value):
    if value == 'True':
        return True
    return False

class UserListApiView(APIView):

    def get(self, request):
        infosuser= UserProfile.objects.all()
        serializer = InfoUserSerializer(infosuser, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):

        data = {
            'username': request.data.get('username'),
            'email': request.data.get('email'),
            'password': request.data.get('password'),
            'is_superuser': bool_convert(request.data.get('is_superuser')),
            'argent': request.data.get('argent'),
        }

        serializer = InfoUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDetailApiView(APIView):

    def get(self, request, id, *args, **kwargs):
        users= UserProfile.objects.get(id=id)
        if not users:
            return Response({"response": f"UserProfile with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = InfoUserSerializer(users)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def delete(self, request, id, *args, **kwargs):
        users= UserProfile.objects.get(id=id)
        if not users:
            return Response({"response": f"UserProfile with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        users.delete()
        return Response({"response": f"UserProfile with id #{id} deleted successfully"}, status=status.HTTP_200_OK)
    
    def put(self, request, id, *args, **kwargs):
        users= UserProfile.objects.get(id=id)
        if not users:
            return Response({"response": f"UserProfile with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            'username': request.data.get('username'),
            'email': request.data.get('email'),
            'password': request.data.get('password'),
            'is_superuser': bool_convert(request.data.get('is_superuser')),
            'argent': request.data.get('argent'),
        }
        
        serializer = InfoUserSerializer(instance=UserProfile, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)