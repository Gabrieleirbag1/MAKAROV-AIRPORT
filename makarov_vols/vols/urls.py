from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('infos/', views.VolListApiView.as_view()),
    path('infos/<int:id>/', views.VolDetailApiView.as_view()),
]