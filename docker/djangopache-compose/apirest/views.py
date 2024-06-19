from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Commentaire
from .serializer import CommentaireSerializer
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

class CommentaireListApiView(APIView):

    def get(self, request):
        commentaires = Commentaire.objects.all()
        serializer = CommentaireSerializer(commentaires, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = {
            'titre': request.data.get('titre'),
            'commentaire': request.data.get('commentaire'),
        }

        serializer = CommentaireSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommentaireDetailApiView(APIView):

    def get(self, request, id, *args, **kwargs):
        commentaire = Commentaire.objects.get(id=id)
        if not commentaire:
            return Response({"response": f"Commentaire with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentaireSerializer(commentaire)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def delete(self, request, id, *args, **kwargs):
        commentaire = Commentaire.objects.get(id=id)
        if not commentaire:
            return Response({"response": f"Commentaire with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        commentaire.delete()
        return Response({"response": f"Commentaire with id #{id} deleted successfully"}, status=status.HTTP_200_OK)
    
    def put(self, request, id, *args, **kwargs):
        commentaire = Commentaire.objects.get(id=id)
        if not commentaire:
            return Response({"response": f"Commentaire with id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            'titre': request.data.get('titre'),
            'commentaire': request.data.get('commentaire'),
        }

        serializer = CommentaireSerializer(instance=commentaire, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
