from django.urls import path, include
from . import views

urlpatterns = [
    path('api/', views.CommentaireListApiView.as_view(), name='commentaire_list'),
    path('api/<int:id>/', views.CommentaireDetailApiView.as_view(), name='commentaire_detail'),
]