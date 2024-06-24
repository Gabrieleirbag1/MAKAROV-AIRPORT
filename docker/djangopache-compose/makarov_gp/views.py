from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.utils import translation
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreationForm, UserModificationForm, AirportForm, FlightForm
import requests, json
import time
import random
from .nats_utils import publish_reservation, PublishAnnulationDemande, PublishAnnulationValidation

# Create your views here.
class HOME(TemplateView):
    def defaultHomePage(request):
        
        if request.method == "POST":
            print("POSTING THE FILTER FORM")
            airports = requests.get('http://172.21.0.4:8004/structure/infos/aeroports/')
            airports = airports.json()
            #print(f"Airports : {airports}")

            flights = requests.get('http://172.21.0.2:8002/vols/infos/')
            flights = flights.json()
            #print(f"Flights : {flights}")

            # Create a dictionary to quickly lookup airport names by id
            airport_dict = {airport['id']: airport['nom'] for airport in airports}

            # Add new attributes to each flight
            for flight in flights:
                flight['aeroport_depart_nom'] = airport_dict.get(flight['aeroport_depart_ref'], 'Unknown')
                flight['aeroport_arrivee_nom'] = airport_dict.get(flight['aeroport_arrivee_ref'], 'Unknown')

            departure = request.POST.get('departure')
            arrival = request.POST.get('arrival')
            date = request.POST.get('date')
            adults = request.POST.get('adults')
            kids = request.POST.get('kids')
            travel_class = request.POST.get('class')

            filtered_flights = []

            for flight in flights:
                if departure and flight['aeroport_depart_ref'] != int(departure):
                    continue
                if arrival and flight['aeroport_arrivee_ref'] != int(arrival):
                    continue
                if date and flight['date_depart'] != date:
                    continue
                if travel_class and flight['type'] != travel_class:
                    continue

                # If all conditions are satisfied, keep the flight
                filtered_flights.append(flight)

            flights = filtered_flights

            print(f"Flights : {flights}")

            return render(request, 'flights/flight_list.html', {'flights': flights, 'airports': airports})

        airports = requests.get('http://172.21.0.4:8004/structure/infos/aeroports/')
        airports = airports.json()

        return render(request, 'general/index.html', {'airports': airports})
    
    def StaffHomePage(request):
        user = request.session.get('user')
        print(f"User : {user}")
        if user is not None:
            if user['is_superuser'] == True:
                return render(request, 'staff/general/index.html')
            else:
                return redirect('makarov_gp:home')
        else:
            #return to login page
            return redirect('makarov_gp:staff_login')

class FLIGHTS(TemplateView):
    def flightsPage(request, *args, **kwargs):

        airports = requests.get('http://172.21.0.4:8004/structure/infos/aeroports/')
        airports = airports.json()
        #print(f"Airports : {airports}")

        flights = requests.get('http://172.21.0.2:8002/vols/infos/')
        flights = flights.json()
        #print(f"Flights : {flights}")

        # Create a dictionary to quickly lookup airport names by id
        airport_dict = {airport['id']: airport['nom'] for airport in airports}

        # Add new attributes to each flight
        for flight in flights:
            flight['aeroport_depart_nom'] = airport_dict.get(flight['aeroport_depart_ref'], 'Unknown')
            flight['aeroport_arrivee_nom'] = airport_dict.get(flight['aeroport_arrivee_ref'], 'Unknown')


        if request.method == "POST":#If the user selected filters for the search
            print("POSTING THE FILTER FORM")

            print(f"Flights : {flights}")

            departure = request.POST.get('departure')
            arrival = request.POST.get('arrival')
            date = request.POST.get('date')
            adults = request.POST.get('adults')
            kids = request.POST.get('kids')
            travel_class = request.POST.get('class')

            # print(f"Departure: {departure}")
            # print(f"Arrival: {arrival}")
            # print(f"Date: {date}")
            # print(f"Adults: {adults}")
            # print(f"Kids: {kids}")
            # print(f"Travel Class: {travel_class}")

            filtered_flights = []

            for flight in flights:
                if departure and flight['aeroport_depart_ref'] != int(departure):
                    continue
                if arrival and flight['aeroport_arrivee_ref'] != int(arrival):
                    continue
                if date and flight['date_depart'] != date:
                    continue
                if travel_class and flight['type'] != travel_class:
                    continue

                # If all conditions are satisfied, keep the flight
                filtered_flights.append(flight)

            flights = filtered_flights

            print(f"Flights : {flights}")

        return render(request, 'flights/flight_list.html', {'flights': flights, 'airports': airports})

    def flights_user(request):
        user = request.session.get('user')
        if user:
            userName = user.get('username')
            print(f"User ID : {userName}")

            #Make the api call to get all of the user's reservations.
            reservations = requests.get(f'http://172.21.0.3:8003/reservations/infos/user_vols/?user_ref={userName}')
            reservations = reservations.json()

            combined_reservations = []#Holds each pair reservation/vol

            #Now we concatenate the reservation and the flight details
            for reservation in reservations:
                vol_associe = requests.get(f'http://172.21.0.2:8002/vols/infos/?numvol={reservation["vol_ref"]}')
                vol_associe = vol_associe.json()

                # print(f"vol associe : {vol_associe}")
                # print(f"Aeroport depart : {vol_associe[0]['aeroport_depart_ref']}")
                # print(f"Aeroport arrivee : {vol_associe[0]['aeroport_arrivee_ref']}")

                #This part below is just here to retrieve each airport's name
                departure_airport = requests.get(f'http://172.21.0.4:8004/structure/infos/aeroports/{vol_associe[0]["aeroport_depart_ref"]}/')
                departure_airport_data = departure_airport.json()
                arrival_airport = requests.get(f'http://172.21.0.4:8004/structure/infos/aeroports/{vol_associe[0]["aeroport_arrivee_ref"]}/')
                arrival_airport_data = arrival_airport.json()

                vol_associe[0]['aeroport_depart_nom'] = departure_airport_data['nom']
                vol_associe[0]['aeroport_arrivee_nom'] = arrival_airport_data['nom']

                combined_data = {**reservation, **vol_associe[0]}  # Assuming vol_associe returns a list with one dictionary
                combined_reservations.append(combined_data)
                
            #print(f"Reservations + Vols : {combined_reservations}")

            return render(request, 'flights/user_flights.html', {"c_reservations": combined_reservations})
        else:
            return redirect('makarov_gp:home')

    def buy_ticket(request, flight_id):#flight_id is the flight number (numvol)
        #Make the api call here to get the flight details

        user = request.session.get('user')
        if user is None:
            message = "You need to be logged-in in order to book a flight !"
            alert = "alert alert-warning"
            return render(request, "flights/message_confirmation.html", {'message': message, 'alert_style': alert})

        response = requests.get(f'http://172.21.0.2:8002/vols/infos/?numvol={flight_id}')
        flight = response.json()
        flight = flight[0]
        
        print(f"Flight : {flight}")

        #Now we get the name for the departure and arrival airports
        departure_airport = requests.get(f'http://172.21.0.4:8004/structure/infos/aeroports/{flight["aeroport_depart_ref"]}/')
        departure_airport_data = departure_airport.json()

        arrival_airport = requests.get(f'http://172.21.0.4:8004/structure/infos/aeroports/{flight["aeroport_arrivee_ref"]}/')
        arrival_airport_data = arrival_airport.json()

        flight['aeroport_depart_nom'] = departure_airport_data['nom']
        flight['aeroport_arrivee_nom'] = arrival_airport_data['nom']

        #Now we render the page with all these infos to inform the user the flight has been booked !
        result = publish_reservation(flight_id, request.session.get('user').get('username'))
        print(f"Result unflitered : {result}")
        try:
            result = json.loads(result)
            if result['status'] == 'True':
                return render(request, 'flights/flight_detail.html', {'flight': flight})
            else:
                message = "Your bank rejected the payement."
                alert = "alert alert-warning"
                return render(request, "flights/message_confirmation.html", {'message': message, 'alert_style': alert})
        except json.decoder.JSONDecodeError:
            message = "Your bank rejected the payement."
            alert = "alert alert-warning"
            return render(request, "flights/message_confirmation.html", {'message': message, 'alert_style': alert})
            
    def cancel_resa(request, flight_id):#flight_id is the flight number (numvol)
        flight_id = flight_id

        #make api call to service to cancel the reservation.
        response = PublishAnnulationDemande(numvol=flight_id, username=request.session.get('user').get('username')).setup()
        response = json.loads(response)
        print(f"Response -> {response}")
        print(f"Response type -> {type(response)}")

        if response['status'] == 'True':
            print("OK OK")
            message = "Your demand has been processed successfully. You will be refunded shortly if a staff member accepts your request."
            alert = "alert alert-success"
        else:
            print("KO KO") 
            message = "Your demand could not be processed. Please try again later."
            alert = "alert alert-warning"

        return render(request, "flights/message_confirmation.html", {'message': message, 'alert_style': alert})

    def addFlight(request):
        if request.method == "POST":
            form = FlightForm(request.POST)
            aeroport_depart_ref = request.POST.get('departure')
            aeroport_arrivee_ref = request.POST.get('arrival')
            date_depart = request.POST.get('date_depart')
            date_arrivee = request.POST.get('date_arrivee')
            heure_depart = request.POST.get('heure_depart')
            heure_arrivee = request.POST.get('heure_arrivee')
            prix = request.POST.get('prix')
            type = request.POST.get('type')
            avion_ref = request.POST.get('plane')

            data = {
                "aeroport_depart_ref": int(aeroport_depart_ref),
                "aeroport_arrivee_ref": int(aeroport_arrivee_ref),
                "date_depart": date_depart,
                "date_arrivee": date_arrivee,
                "heure_depart": heure_depart,
                "heure_arrivee": heure_arrivee,
                "prix": int(prix),
                "type": type,
                "avion_ref": avion_ref
            }

            print(f"Data to send : {data}")

            response = requests.post(
                'http://172.21.0.2:8002/vols/infos/',
                json=data,
                headers={'Content-Type': 'application/json'}
            )

            print(f"API response status: {response.status_code}")

            if response.status_code == 201:
                message = "Flight successfully added !"
                form = FlightForm()
            else:
                message = "Error while adding the flight, please retry later on.."
            
            airports = requests.get('http://172.21.0.4:8004/structure/infos/aeroports/')
            airports = airports.json()
            planes = requests.get('http://172.21.0.4:8004/structure/infos/avions/')
            planes = planes.json()
            return render(request, 'staff/flights/add_flight.html', {'form': form, 'airports':airports, "planes":planes, "message":message})
        else:
            form = FlightForm()
            airports = requests.get('http://172.21.0.4:8004/structure/infos/aeroports/')
            airports = airports.json()
            planes = requests.get('http://172.21.0.4:8004/structure/infos/avions/')
            planes = planes.json()

            return render(request, 'staff/flights/add_flight.html', {'form': form, 'airports':airports, "planes":planes})

    def showFlights(request):
        airports = requests.get('http://172.21.0.4:8004/structure/infos/aeroports/')
        airports = airports.json()
        flights = requests.get('http://172.21.0.2:8002/vols/infos/')
        flights = flights.json()

        # Create a dictionary to quickly lookup airport names by id
        airport_dict = {airport['id']: airport['nom'] for airport in airports}

        # Add new attributes to each flight
        for flight in flights:
            flight['aeroport_depart_nom'] = airport_dict.get(flight['aeroport_depart_ref'], 'Unknown')
            flight['aeroport_arrivee_nom'] = airport_dict.get(flight['aeroport_arrivee_ref'], 'Unknown')

        return render(request, 'staff/flights/show_flights.html', {'flights': flights})

    def del_flight(request, flight_id):
        response = requests.delete(f'http://172.21.0.2:8002/vols/infos/{flight_id}/')

        if response.status_code == 200:
            message = "This flight has been deleted successfully."
        else:
            message = "The flight could not be deleted. Please try again later."

        airports = requests.get('http://172.21.0.4:8004/structure/infos/aeroports/')
        airports = airports.json()
        flights = requests.get('http://172.21.0.2:8002/vols/infos/')
        flights = flights.json()

        # Create a dictionary to quickly lookup airport names by id
        airport_dict = {airport['id']: airport['nom'] for airport in airports}

        # Add new attributes to each flight
        for flight in flights:
            flight['aeroport_depart_nom'] = airport_dict.get(flight['aeroport_depart_ref'], 'Unknown')
            flight['aeroport_arrivee_nom'] = airport_dict.get(flight['aeroport_arrivee_ref'], 'Unknown')

        return render(request, 'staff/flights/show_flights.html', {'flights': flights, "message":message})

    def edit_flight(request, flight_id):
        if request.method == "POST":
            form = FlightForm(request.POST)
            aeroport_depart_ref = request.POST.get('departure')
            aeroport_arrivee_ref = request.POST.get('arrival')
            date_depart = request.POST.get('date_depart')
            date_arrivee = request.POST.get('date_arrivee')
            heure_depart = request.POST.get('heure_depart')
            heure_arrivee = request.POST.get('heure_arrivee')
            prix = request.POST.get('prix')
            type = request.POST.get('type')
            avion_ref = request.POST.get('plane')

            data = {
                "aeroport_depart_ref": int(aeroport_depart_ref),
                "aeroport_arrivee_ref": int(aeroport_arrivee_ref),
                "date_depart": date_depart,
                "date_arrivee": date_arrivee,
                "heure_depart": heure_depart,
                "heure_arrivee": heure_arrivee,
                "prix": int(prix),
                "type": type,
                "avion_ref": avion_ref
            }

            print(f"Data to send : {data}")

            response = requests.put(
                f'http://172.21.0.2:8002/vols/infos/{flight_id}/',
                json=data,
                headers={'Content-Type': 'application/json'}
            )

            print(f"API response status: {response.status_code}")

            flight = requests.get(f'http://172.21.0.2:8002/vols/infos/{flight_id}/')
            flight = flight.json()
            form = FlightForm(flight)

            airports = requests.get('http://172.21.0.4:8004/structure/infos/aeroports/')
            airports = airports.json()
            planes = requests.get('http://172.21.0.4:8004/structure/infos/avions/')
            planes = planes.json()

            if response.status_code == 200:
                message = "The flight has been modified !"
            else:
                message = "There was a problem while modifying this flight. Please retry later on."
            return render(request, 'staff/flights/edit_flight.html', {"form": form, "airports":airports, "planes":planes, "flight": flight, "message":message})
        else:
            flight = requests.get(f'http://172.21.0.2:8002/vols/infos/{flight_id}/')
            flight = flight.json()
            form = FlightForm(flight)

            airports = requests.get('http://172.21.0.4:8004/structure/infos/aeroports/')
            airports = airports.json()
            planes = requests.get('http://172.21.0.4:8004/structure/infos/avions/')
            planes = planes.json()

            return render(request, 'staff/flights/edit_flight.html', {"form": form, "airports":airports, "planes":planes, "flight": flight})

class USERS(TemplateView):
    def loginPage(request):
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password')

            print(f"USERNAME == {username} PASSWORD == {password}")

            #API CALL TO AUTH THE USER
            response = requests.post('http://172.21.0.8:8001/users/login/users/',
                    json={'username': username, 'password': password},
                    headers={'COntent-Type': 'application/json'}
            )

            if response.status_code == 200:
                user_data = response.json()
                if user_data.get('username') == username:
                    request.session['user'] = {
                        'id': user_data['id'],
                        'username': user_data['username'],
                        'first_name': user_data['first_name'],
                        'last_name': user_data['last_name'],
                        'email': user_data['email'],
                        'auth': True,
                    }
                    return redirect('makarov_gp:home')
            else:
                form.add_error(None, 'Invalid login credentials.')
                return render(request, 'users/login.html', {'form': form})
        else:
            form = AuthenticationForm()
            
        return render(request, 'users/login.html', {'form': form})
    
    def registerPage(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)

            first_name = request.POST.get('first_name') 
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')

            data = {
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
                "password": password,
                "email": email,
            }

            print(f"Data to send : {data}")
            response = requests.post(
                'http://172.21.0.8:8001/users/infos/users/',
                json=data,
                headers={'Content-Type': 'application/json'}
            )

            print(f"API response status: {response.status_code}")

            if response.status_code == 201:
                # User created successfully, redirect to home
                user_data = response.json()
                request.session['user'] = {
                    'id': user_data['id'],
                    'username': user_data['username'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'email': user_data['email'],
                    'auth': True,
                }
                return redirect("makarov_gp:home")
            else:
                form.add_error(None, 'Error creating user. Please try again.')
                return render(request, 'users/register.html', {'form': form})
        else:
            form = UserCreationForm()
            return render(request, 'users/register.html', {'form': form})
    
    def logoutPage(request):
        request.session.flush()
        return redirect('makarov_gp:home')
    
    def profilePage(request):

        if request.method == 'POST':
            form = UserModificationForm(request.POST)
            user_ID = request.session.get('user').get('id')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')

            data = {
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
                "email": email
            }

            response = requests.put(
                f'http://172.21.0.8:8001/users/infos/users/{user_ID}/', 
                json=data,
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 200:
                print("Info update succesful.")

                user = request.session.get('user', {})
                user.update({
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                })
                request.session['user'] = user

                response_status = {
                    "status": "Success !",
                    "message": "Your informations have been updated successfully."
                }

                print(f"USER ID : {request.session.get('user').get('id')}")
                return render(request, 'users/profile.html', {'user': data, 'form':form, 'response_status': response_status})
            else:
                print("Error while updating user's infos")
                response_status = {
                    "status": "Something went wrong ! !",
                    "message": "There has been a problem with the update. Please try again later."
                }
                return render(request, 'users/profile.html', {'user': data, 'form':form, 'response_status': response_status})
        else:
            print(f"\n\nDefault page\n\n")
            user = request.session.get('user')

            data = {
                "first_name": user.get('first_name'),
                "last_name": user.get('last_name'),
                "username": user.get('username'),
                "email": user.get('email')
            }

            form = UserModificationForm(data=data)

        return render(request, 'users/profile.html', {'user': data, 'form':form})

class CancelDemands(TemplateView):
    def show_demands(request):
        demands_unfiltered = requests.get('http://172.21.0.3:8003/reservations/infos/')
        demands_unfiltered = demands_unfiltered.json()

        #print(f"demands_unfiltered -> {demands_unfiltered}")

        demands_filtered = [demand for demand in demands_unfiltered if demand['demande'] and not demand['annulation']]

        return render(request, 'staff/demands/show_demands.html', {'demands': demands_filtered})
    
    def show_user_detail(request, userName):
        user = requests.get(f'http://172.21.0.8:8001/users/infos/users/?username={userName}')
        user_list = user.json()

        if user_list:
            user = user_list[0]
        else:
            user = None

        return render(request, 'staff/demands/show_user_details.html', {"user":user})

    def show_flight_detail(request, numvol):
        flight = requests.get(f'http://172.21.0.2:8002/vols/infos/?numvol={numvol}')
        flight_list = flight.json()

        if flight_list:
            flight = flight_list[0]
        else:
            flight = None

        airport_depart = requests.get(f"http://172.21.0.4:8004/structure/infos/aeroports/{flight['aeroport_depart_ref']}/")
        airport_arrivee =  requests.get(f"http://172.21.0.4:8004/structure/infos/aeroports/{flight['aeroport_arrivee_ref']}/")

        airport_depart = airport_depart.json()
        airport_arrivee = airport_arrivee.json()

        flight['aeroport_depart_nom'] = airport_depart['nom']
        flight['aeroport_arrivee_nom'] = airport_arrivee['nom']

        print(f"Flight : {flight}")

        return render(request, 'staff/demands/show_flight_details.html', {"flight":flight})

    def validate_demand(request, numvol, username):
        reponse = PublishAnnulationValidation(numvol=numvol, annulation="True", username=username).setup()

        return redirect('makarov_gp:show_demands')

    def reject_demand(request, numvol, username):
        reponse = PublishAnnulationValidation(numvol=numvol, annulation="False", username=username).setup()

        return redirect('makarov_gp:show_demands')

class STAFF(TemplateView):
    def registerPage(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)

            first_name = request.POST.get('first_name') 
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            airport_id = request.POST.get('airport')

            data = {
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
                "password": password,
                "email": email,
            }

            print(f"Data to send : {data}")

            #Start by creating regular user
            response = requests.post(
                'http://172.21.0.8:8001/users/infos/users/',
                json=data,
                headers={'Content-Type': 'application/json'}
            )

            print(f"API response status: {response.status_code}")

            if response.status_code == 201:
                # User created successfully
                user_data = response.json()

                #upgrade him to staff
                staff_data = {
                    "user_ref": user_data['username'],
                    "aeroport_ref": int(airport_id),
                    "level": 1
                }

                response = requests.post(
                    'http://172.21.0.4:8004/structure/infos/staff/',
                    json=staff_data,
                    headers={'Content-Type': 'application/json'}
                )

                print(f"API response status: {response.status_code}")
                if response.status_code == 201:
                    staff_data = response.json()

                    print(f"Staff data : {staff_data}")
                    print(f"User data : {user_data}")

                    #set the session vars to log him in
                    request.session['user'] = {
                        'id': user_data['id'],
                        'username': user_data['username'],
                        'first_name': user_data['first_name'],
                        'last_name': user_data['last_name'],
                        'email': user_data['email'],
                        'auth': True,
                        'is_superuser': True,
                    }
                    return redirect("makarov_gp:home_staff")
                else:
                    print("Error while creating staff member")
                    form.add_error(None, 'Error creating user. Please try again.')
                    return render(request, 'staff/register.html', {'form': form})
                #get him to the home page
            else:
                form.add_error(None, 'Error creating user. Please try again.')
                return render(request, 'staff/register.html', {'form': form})
        else:
            airports = requests.get('http://172.21.0.4:8004/structure/infos/aeroports/')
            airports = airports.json()

            form = UserCreationForm()
            return render(request, 'staff/register.html', {'form': form, 'airports': airports})

    def loginPage(request):
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password')

            print(f"USERNAME == {username} PASSWORD == {password}")

            #API CALL TO AUTH THE USER
            response = requests.post('http://172.21.0.8:8001/users/login/users/',
                    json={'username': username, 'password': password},
                    headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 200:
                user_data = response.json()
                print(f"User data : {user_data}")
                if user_data.get('is_superuser') == True:
                    request.session['user'] = {
                        'id': user_data['id'],
                        'username': user_data['username'],
                        'first_name': user_data['first_name'],
                        'last_name': user_data['last_name'],
                        'email': user_data['email'],
                        'auth': True,
                        'is_superuser': True,
                    }
                    return redirect('makarov_gp:home_staff')
            else:
                form.add_error(None, 'Invalid login credentials.')
                return render(request, 'users/login.html', {'form': form})
        else:
            form = AuthenticationForm()

        return render(request, 'users/login.html', {'form': form})

    def profilePage(request):
        if request.method == 'POST':
            form = UserModificationForm(request.POST)
            user_ID = request.session.get('user').get('id')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')

            data = {
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
                "email": email
            }

            response = requests.put(
                f'http://172.21.0.8:8001/users/infos/users/{user_ID}/', 
                json=data,
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 200:
                print("Info update succesful.")

                user = request.session.get('user', {})
                user.update({
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'is_superuser': True,
                })
                request.session['user'] = user

                response_status = {
                    "status": "Success !",
                    "message": "Your informations have been updated successfully."
                }

                print(f"USER ID : {request.session.get('user').get('id')}")
                return render(request, 'users/user_profile.html', {'user': data, 'form':form, 'response_status': response_status})
            else:
                print("Error while updating user's infos")
                response_status = {
                    "status": "Something went wrong ! !",
                    "message": "There has been a problem with the update. Please try again later."
                }
                return render(request, 'users/user_profile.html', {'user': data, 'form':form, 'response_status': response_status})
        else:
            print(f"\n\nDefault page\n\n")
            user = request.session.get('user')

            data = {
                "first_name": user.get('first_name'),
                "last_name": user.get('last_name'),
                "username": user.get('username'),
                "email": user.get('email')
            }

            form = UserModificationForm(data=data)

        return render(request, 'users/user_profile.html', {'user': data, 'form':form})

class AIRPORTS(TemplateView):
    def addAirport(request):
        if request.method == 'POST':
            form = AirportForm(request.POST)
            nom = request.POST.get('nom')
            code_pays = request.POST.get('code_pays')
            fuseau = request.POST.get('fuseau')

            data = {
                "nom": nom,
                "code_pays": code_pays,
                "fuseau": fuseau
            }

            print(f"Data to send : {data}")

            response = requests.post('http://172.21.0.4:8004/structure/infos/aeroports/',
                    json=data,
                    headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 201:
                # Airport created successfully
                print("add succesful")
                form = AirportForm()

                message = "The airport has been succesfully added to the database."

                return render(request, 'staff/airports/add_airport.html', {'form':form, "message":message})
            else:
                form.add_error(None, 'Error creating airport. Please try again.')
                return render(request, 'staff/airports/add_airport.html', {'form': form})
        else:
            form = AirportForm()
            return render(request, 'staff/airports/add_airport.html', {'form': form})

    def showAirports(request):
        airports = requests.get('http://172.21.0.4:8004/structure/infos/aeroports/')
        airports = airports.json()

        print(f"Airports : {airports}")

        return render(request, 'staff/airports/show_airports.html', {'airports': airports})

    def del_airport(request, airport_id):
        response = requests.delete(f'http://172.21.0.4:8004/structure/infos/aeroports/{airport_id}/')

        print(f"Response : {response.status_code}")
        
        airports = requests.get('http://172.21.0.4:8004/structure/infos/aeroports/')
        airports = airports.json()

        if response.status_code == 200:
            message = "The airport has been deleted successfully."
        else:
            message = "The airport could not be deleted. Please try again later."

        return render(request, 'staff/airports/show_airports.html', {'airports': airports, 'message': message})
    
    def edit_airport(request, airport_id):
        if request.method == "POST":
            form = AirportForm(request.POST)
            nom = request.POST.get('nom')
            code_pays = request.POST.get('code_pays')
            fuseau = request.POST.get('fuseau')

            data = {
                "nom": nom,
                "code_pays": code_pays,
                "fuseau": fuseau
            }

            response = requests.put(
                f'http://172.21.0.4:8004/structure/infos/aeroports/{airport_id}/',
                json=data,
                headers={'Content-Type': 'application/json'}
                )
            
            print(f"response : {response}")

            if response.status_code == 200:
                message = "The airport has been updated successfully."
            else:
                message = "The airport could not be updated. Please try again later."
            return render(request, 'staff/airports/edit_airport.html', {'form': form, 'message': message})
        else:
            airport = requests.get(f'http://172.21.0.4:8004/structure/infos/aeroports/{airport_id}/')
            airport = airport.json()

            form = AirportForm(data=airport)
            return render(request, 'staff/airports/edit_airport.html', {'form': form})