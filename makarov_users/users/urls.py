from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('infos/', views.UserListApiView.as_view(), name='infos_list'),
    path('infos/<int:id>/', views.UserDetailApiView.as_view(), name='infos_detail'),
]