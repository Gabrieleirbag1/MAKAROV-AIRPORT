from .models import UserProfile, Banque
from .serializer import InfoUserSerializer, InfoBanqueSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate
import requests, json, random
from .nats_utils import PublishBank
from copy import deepcopy

# Create your views here.
def index(request):
    response = PublishBank().setup()
    print(response)
    return HttpResponseRedirect('infos/')

def bool_convert(value):
    if value == 'True':
        return True
    return False

class UserListApiView(APIView):

    def get(self, request):
        username = request.query_params.get('username')
        if username is not None:
            infosuser= UserProfile.objects.filter(username=username)
            print(infosuser)
        else:
            infosuser= UserProfile.objects.all()
        serializer = InfoUserSerializer(infosuser, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):

        data = {
            'username': request.data.get('username'),
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'email': request.data.get('email'),
            'password': request.data.get('password'),
        }

        serializer = InfoUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            self.post_bank_info(request.data.get('username'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post_bank_info(self, username):
        argent = random.randint(800, 3000)
        rib = random.randint(00000000, 99999999)
        url = 'http://172.21.0.1:8000/users/infos/banque/'
        data = {
            'username': username,
            'argent': argent,
            'rib': rib
        }
        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, data=json.dumps(data), headers=headers)
        
        if response.status_code == 201:
            print('Information de la banque créée avec succès.')
        else:
            print(f'Erreur lors de la création de l\'information de la banque: {response.content}')
    
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
        try:
            user = UserProfile.objects.get(id=id)
        except UserProfile.DoesNotExist:
            return Response({"response": f"UserProfile with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        old_username = deepcopy(user.username)
        data = {
            'username': request.data.get('username', user.username),
            'first_name': request.data.get('first_name', user.first_name),
            'last_name': request.data.get('last_name', user.last_name),
            'email': request.data.get('email', user.email),
            'password': request.data.get('password', user.password),
        }

        serializer = InfoUserSerializer(instance=user, data=data, partial=True)

        if serializer.is_valid():
            response = requests.get(f"http://172.21.0.1:8000/users/infos/banque/?username={old_username}")
            id = response.json()[0]['id']
            response = requests.get(f"http://172.21.0.4:8000/structure/infos/staff/?user_ref={old_username}")
            id_staff = response.json()[0]['id']

            headers = {'Content-Type': 'application/json'}

            data = {
                'username': request.data.get('username', user.username),
            }
            response = requests.put(f"http://172.21.0.1:8000/users/infos/banque/{id}/", data=json.dumps(data), headers=headers)
            
            data = {
                'user_ref': request.data.get('username', user.username),
            }
            response = requests.put(f"http://172.21.0.4:8000/structure/infos/staff/{id_staff}/", data=json.dumps(data), headers=headers)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#############################################################""
class SuperUserApiView(APIView):

    def get(self, request):
        username = request.query_params.get('username')
        if username is not None:
            infosuser= UserProfile.objects.filter(username=username)
            print(infosuser)
        else:
            infosuser= UserProfile.objects.all()
        serializer = InfoUserSerializer(infosuser, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        return

class SuperUserDetailApiView(APIView):

    def get(self, request, id, *args, **kwargs):
        users= UserProfile.objects.get(id=id)
        if not users:
            return Response({"response": f"UserProfile with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = InfoUserSerializer(users)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id, *args, **kwargs):
        try:
            user = UserProfile.objects.get(id=id)
        except UserProfile.DoesNotExist:
            return Response({"response": f"UserProfile with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            'is_superuser': request.data.get('is_superuser', user.is_superuser)
        }

        serializer = InfoUserSerializer(instance=user, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#####################""
class LoginUserListApiView(APIView):

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        infos = requests.get(f"http://172.21.0.1:8000/users/infos/users/?username={username}")
        infos = infos.json()
        try:
            if username == infos[0]['username'] and password == infos[0]['password']:
                infosuser = UserProfile.objects.get(username=username)
                serializer = InfoUserSerializer(infosuser)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)
        except IndexError:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)
#######################################################""

class BanqueListApiView(APIView):

    def get(self, request):
        username = request.query_params.get('username')
        if username is not None:
            infosbanque= Banque.objects.filter(username=username)
            print(infosbanque)
        else:
            infosbanque= Banque.objects.all()
        serializer = InfoBanqueSerializer(infosbanque, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):

        data = {
            'username': request.data.get('username'),
            'argent': request.data.get('argent'),
            'rib': request.data.get('rib'),
        }

        serializer = InfoBanqueSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BanqueDetailApiView(APIView):
    
    def get(self, request, id, *args, **kwargs):
        banques= Banque.objects.get(id=id)
        if not banques:
            return Response({"response": f"Banque with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = InfoBanqueSerializer(banques)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def delete(self, request, id, *args, **kwargs):
        banques= Banque.objects.get(id=id)
        if not banques:
            return Response({"response": f"Banque with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        banques.delete()
        return Response({"response": f"Banque with id #{id} deleted successfully"}, status=status.HTTP_200_OK)
    
    def put(self, request, id, *args, **kwargs):
        try:
            banques = Banque.objects.get(id=id)
        except Banque.DoesNotExist:
            return Response({"response": f"Banque with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            'username': request.data.get('username') or banques.username,
            'argent': request.data.get('argent') or banques.argent,
            'rib': request.data.get('rib') or banques.rib,
        }
        
        serializer = InfoBanqueSerializer(instance=banques, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RibBanqueListApiView(APIView):

    def get(self, request):
        rib = request.query_params.get('rib')
        if rib is not None:
            infosbanque= Banque.objects.filter(rib=rib)
            print(infosbanque)
        else:
            infosbanque= Banque.objects.all()
        serializer = InfoBanqueSerializer(infosbanque, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)