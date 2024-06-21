from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('infos/', views.ReservationsListApiView.as_view()),
    path('infos/<int:id>/', views.ReservationsDetailApiView.as_view()),
    
    path('infos/user_vols/', views.UserVolsListApiView.as_view()),
]