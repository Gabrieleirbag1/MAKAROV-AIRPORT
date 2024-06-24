from django.contrib import admin
from django.urls import path
from . import views

app_name = 'makarov_gp'

urlpatterns = [
    #-------------------GENERAL----------------------
    path('home/', views.HOME.defaultHomePage, name='home'),

    #-------------------USERS----------------------
    path('login/', views.USERS.loginPage, name='login'),
    path('logout/', views.USERS.logoutPage, name='logout'),
    path('register/', views.USERS.registerPage, name='register'),
    path('profile/', views.USERS.profilePage, name='profile'),
    path('flights/', views.FLIGHTS.flightsPage, name='flights'),
    path('flights_user/', views.FLIGHTS.flights_user, name="flights_user"),
    path('buy_ticket/<int:flight_id>/', views.FLIGHTS.buy_ticket, name='buy_ticket'),
    path('cancel_resa/<int:flight_id>/', views.FLIGHTS.cancel_resa, name='cancel_resa'),

    path('staff/register/', views.STAFF.registerPage, name='staff_register'),
    path('staff/login/', views.STAFF.loginPage, name='staff_login'),
    path('staff/profile/', views.STAFF.profilePage, name='staff_profile'),
    path('staff/home/', views.HOME.StaffHomePage, name="home_staff"),
    path('staff/airports/', views.AIRPORTS.addAirport, name="addAirport"),
    path('staff/airports/all/', views.AIRPORTS.showAirports, name="showAirports"),
    path('staff/airports/delete/<int:airport_id>/', views.AIRPORTS.del_airport, name="del_airport"),
    path('staff/airports/edit/<int:airport_id>/', views.AIRPORTS.edit_airport, name="edit_airport"),
    path('staff/flights/', views.FLIGHTS.addFlight, name="addFlight"),
    path('staff/flights/all/', views.FLIGHTS.showFlights, name="showFlights"),
    path('staff/flights/delete/<int:flight_id>/', views.FLIGHTS.del_flight, name="del_flight"),
    path('staff/flights/edit/<int:flight_id>/', views.FLIGHTS.edit_flight, name='edit_flight'),
    path('staff/demands/', views.CancelDemands.show_demands, name="show_demands"),
    path('staff/show_user_detail/<str:userName>', views.CancelDemands.show_user_detail, name="show_user_detail"),
    path('staff/show_flight_detail/<int:numvol>', views.CancelDemands.show_flight_detail, name="show_flight_detail"),
    path('staff/validate_demand/<int:numvol>/<str:username>/', views.CancelDemands.validate_demand, name="validate_demand"),
    path('staff/reject_demand/<int:numvol>/<str:username>/', views.CancelDemands.reject_demand, name="reject_demand"),
]
