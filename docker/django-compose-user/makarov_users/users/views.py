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
    """index() : redirige vers la page d'informations de vol
    
    Args:
        request (HttpRequest): requête HTTP"""
    response = PublishBank().setup()
    print(response)
    return HttpResponseRedirect('infos/')

def bool_convert(value):
    """bool_convert() : convertit une chaine de caractère en booléen
    
    Args:
        value (str): chaine de caractère à convertir"""
    if value == 'True':
        return True
    return False

class UserListApiView(APIView):
    """UserListApiView() : Vue pour la gestion des utilisateurs"""
    def get(self, request):
        """get() : get tous les enregistrements d'utilisateurs ou un enregistrement d'utilisateur par username
        
        Args:
            request (HttpRequest): requête HTTP"""
        username = request.query_params.get('username')
        if username is not None:
            infosuser= UserProfile.objects.filter(username=username)
            print(infosuser)
        else:
            infosuser= UserProfile.objects.all()
        serializer = InfoUserSerializer(infosuser, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        """post() : crée un nouvel enregistrement d'utilisateur
        
        Args:
            request (HttpRequest): requête HTTP"""
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
        """post_bank_info() : crée un nouvel enregistrement d'information de la banque
        
        Args:
            username (str): nom d'utilisateur de l'utilisateur"""
        argent = random.randint(800, 3000)
        rib = random.randint(00000000, 99999999)
        url = 'http://172.21.0.8:8001/users/infos/banque/'
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
    """UserDetailApiView() : Vue pour les informations d'un utilisateur"""
    def get(self, request, id, *args, **kwargs):
        """get() : get les informations d'un utilisateur
        
        Args:
            request (HttpRequest): requête HTTP
            id (int): id de l'utilisateur à récupérer"""
        users= UserProfile.objects.get(id=id)
        if not users:
            return Response({"response": f"UserProfile with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = InfoUserSerializer(users)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def delete(self, request, id, *args, **kwargs):
        """delete() : supprime les informations d'un utilisateur
        
        Args:
            request (HttpRequest): requête HTTP
            id (int): id de l'utilisateur à supprimer"""
        users= UserProfile.objects.get(id=id)
        if not users:
            return Response({"response": f"UserProfile with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        users.delete()
        return Response({"response": f"UserProfile with id #{id} deleted successfully"}, status=status.HTTP_200_OK)
    
    def put(self, request, id, *args, **kwargs):
        """put() : update les informations d'un utilisateur
        
        Args:
            request (HttpRequest): requête HTTP
            id (int): id de l'utilisateur à mettre à jour"""
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
            response = requests.get(f"http://172.21.0.8:8001/users/infos/banque/?username={old_username}")
            id = response.json()[0]['id']
            try :
                response = requests.get(f"http://172.21.0.4:8004/structure/infos/staff/?user_ref={old_username}")
                id_staff = response.json()[0]['id']
            except IndexError:
                id_staff = None
            try :
                ids_res = []
                response = requests.get(f"http://172.21.0.3:8003/reservations/infos/user_vols/?user_ref={old_username}")
                reservations = response.json()
                for reservation in reservations:
                    ids_res.append(reservation['id'])
            except IndexError:
                print("error")
                ids_res = None

            headers = {'Content-Type': 'application/json'}

            data = {
                'username': request.data.get('username', user.username),
            }
            response = requests.put(f"http://172.21.0.8:8001/users/infos/banque/{id}/", data=json.dumps(data), headers=headers)
            
            if id_staff:
                data = {
                    'user_ref': request.data.get('username', user.username),
                }
                response = requests.put(f"http://172.21.0.4:8004/structure/infos/staff/{id_staff}/", data=json.dumps(data), headers=headers)

            if ids_res:
                data = {
                    'user_ref': request.data.get('username', user.username),
                }
                for id_res in ids_res:
                    response = requests.put(f"http://172.21.0.3:8003/reservations/infos/{id_res}/", data=json.dumps(data), headers=headers)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#############################################################""
class SuperUserApiView(APIView):
    """SuperUserApiView() : Vue pour les informations d'un super utilisateur"""
    def get(self, request):
        """get() : get tous les enregistrements d'utilisateurs ou un enregistrement d'utilisateur par username
        
        Args:
            request (HttpRequest): requête HTTP"""
        username = request.query_params.get('username')
        if username is not None:
            infosuser= UserProfile.objects.filter(username=username)
            print(infosuser)
        else:
            infosuser= UserProfile.objects.all()
        serializer = InfoUserSerializer(infosuser, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """post() : crée un nouvel enregistrement d'utilisateur
        
        Args:
            request (HttpRequest): requête HTTP"""
        return

class SuperUserDetailApiView(APIView):
    """SuperUserDetailApiView() : Vue pour les informations d'un super utilisateur"""
    def get(self, request, id, *args, **kwargs):
        """get() : get les informations d'un utilisateur
        
        Args:
            request (HttpRequest): requête HTTP
            id (int): id de l'utilisateur à récupérer"""
        users= UserProfile.objects.get(id=id)
        if not users:
            return Response({"response": f"UserProfile with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = InfoUserSerializer(users)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id, *args, **kwargs):
        """put() : update les informations d'un utilisateur
        
        Args:
            request (HttpRequest): requête HTTP
            id (int): id de l'utilisateur à mettre à jour"""
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
    """LoginUserListApiView() : Vue pour la connexion d'un utilisateur"""
    def post(self, request, *args, **kwargs):
        """post() : connecte un utilisateur
        
        Args:
            request (HttpRequest): requête HTTP"""
        username = request.data.get('username')
        password = request.data.get('password')

        infos = requests.get(f"http://172.21.0.8:8001/users/infos/users/?username={username}")
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
    """BanqueListApiView() : Vue pour la gestion des informations de la banque"""
    def get(self, request):
        """get() : get tous les enregistrements d'informations de la banque ou un enregistrement d'information de la banque par username
        
        Args:
            request (HttpRequest): requête HTTP"""
        username = request.query_params.get('username')
        if username is not None:
            infosbanque= Banque.objects.filter(username=username)
            print(infosbanque)
        else:
            infosbanque= Banque.objects.all()
        serializer = InfoBanqueSerializer(infosbanque, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        """post() : crée un nouvel enregistrement d'information de la banque
        
        Args:
            request (HttpRequest): requête HTTP"""
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
    """BanqueDetailApiView() : Vue pour les informations d'une banque"""
    def get(self, request, id, *args, **kwargs):
        """get() : get les informations d'une banque
        
        Args:
            request (HttpRequest): requête HTTP
            id (int): id de l'information de la banque à récupérer"""
        banques= Banque.objects.get(id=id)
        if not banques:
            return Response({"response": f"Banque with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = InfoBanqueSerializer(banques)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def delete(self, request, id, *args, **kwargs):
        """delete() : supprime les informations d'une banque
        
        Args:
            request (HttpRequest): requête HTTP
            id (int): id de l'information de la banque à supprimer"""
        banques= Banque.objects.get(id=id)
        if not banques:
            return Response({"response": f"Banque with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        banques.delete()
        return Response({"response": f"Banque with id #{id} deleted successfully"}, status=status.HTTP_200_OK)
    
    def put(self, request, id, *args, **kwargs):
        """put() : update les informations d'une banque
        
        Args:
            request (HttpRequest): requête HTTP
            id (int): id de l'information de la banque à mettre à jour"""
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
    """RibBanqueListApiView() : Vue pour la gestion des informations de la banque par rib"""
    def get(self, request):
        """get() : get tous les enregistrements d'informations de la banque ou un enregistrement d'information de la banque par rib
        
        Args:
            request (HttpRequest): requête HTTP"""
        rib = request.query_params.get('rib')
        if rib is not None:
            infosbanque= Banque.objects.filter(rib=rib)
            print(infosbanque)
        else:
            infosbanque= Banque.objects.all()
        serializer = InfoBanqueSerializer(infosbanque, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)