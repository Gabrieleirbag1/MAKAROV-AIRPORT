from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('infos/users/', views.UserListApiView.as_view(), name='infos_list'),
    path('infos/users/<int:id>/', views.UserDetailApiView.as_view(), name='infos_detail'),

    path('login/users/', views.LoginUserListApiView.as_view(), name='login'),

    path('infos/banque/', views.BanqueListApiView.as_view(), name='banque_list'),
    path('infos/banque/<int:id>/', views.BanqueDetailApiView.as_view(), name='banque_detail'),
]