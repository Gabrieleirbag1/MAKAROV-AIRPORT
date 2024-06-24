from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('infos/avions/', views.AvionsListApiView.as_view()),
    path('infos/avions/<int:id>/', views.AvionsDetailApiView.as_view()),

    path('infos/staff/', views.StaffListApiView.as_view()),
    path('infos/staff/<int:id>/', views.StaffDetailApiView.as_view()),

    path('infos/aeroports/', views.AeroportsListApiView.as_view()),
    path('infos/aeroports/<int:id>/', views.AeroportsDetailApiView.as_view()),
]