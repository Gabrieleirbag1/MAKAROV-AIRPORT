import requests

# Define the URL to your Django API endpoint for adding new Avions
API_URL = "http://172.21.0.4:8004/structure/infos/avions/"

# List of avion data to add
avions_data = [
    {"marque": "Boeing", "modele": "777-300ER", "places": 365, "image": None},
    {"marque": "Ilyushin", "modele": "II-96", "places": 300, "image": None},
    {"marque": "Sukhoi", "modele": "SSJ100", "places": 87, "image": None},  # Note: Adjusted places to minimum
    {"marque": "BOEING", "modele": "737-800", "places": 162, "image": None},
    {"marque": "AIRBUS", "modele": "A220-300", "places": 130, "image": None},
    {"marque": "AIRBUS", "modele": "A380", "places": 500, "image": None},
    {"marque": "Boeing", "modele": "747-8 Intercontinental", "places": 467, "image": None},
    {"marque": "Airbus", "modele": "A320", "places": 150, "image": None},
    {"marque": "Airbus", "modele": "A350-900", "places": 325, "image": None},
    {"marque": "Boeing", "modele": "787-9 Dreamliner", "places": 296, "image": None},
    {"marque": "Ilyushin", "modele": "II-86", "places": 350, "image": None},
    {"marque": "Boeing", "modele": "747-400", "places": 416, "image": None},
]

def add_avions(avions):
    for avion in avions:
        response = requests.post(API_URL, data=avion)
        if response.status_code == 201:
            print(f"Successfully added: {avion['marque']} {avion['modele']}")
        else:
            print(f"Failed to add: {avion['marque']} {avion['modele']} - Status Code: {response.status_code}")

add_avions(avions_data)