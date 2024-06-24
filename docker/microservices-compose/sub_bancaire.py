import asyncio
import nats
import json
import os
import requests

async def message_handler(msg):
    """Gère les messages reçus par le serveur NATS.
    
    Args:
        msg (nats.aio.client.Msg): Le message reçu par le serveur NATS."""
    if msg.subject == "banque.*":
        response_data = await banque(msg)
    else:
        response_data = {"status": "ignore"}
    print("reponse", response_data)
    await msg.respond(json.dumps(response_data).encode())

async def banque(msg):
    """Gère les messages reçus par le serveur NATS.
    
    Args:
        msg (nats.aio.client.Msg): Le message reçu par le serveur NATS."""
    async def get_rib(username):
        """Récupère le RIB associé à l'utilisateur.
        
        Args:
            username (str): Le nom d'utilisateur associé à la réponse."""
        user_response = requests.get(f"http://172.21.0.8:8001/users/infos/banque/?username={username}")
        user_data = user_response.json()
        rib = user_data[0]['rib']
        print(rib)
        return rib
    
    async def get_vol_info(numvol):
        """Récupère les informations du vol associé au numéro de vol.
        
        Args:
            numvol (int): Le numéro de vol associé à la réponse."""
        vol_response = requests.get(f"http://172.21.0.2:8002/vols/infos/?numvol={numvol}")
        vol_data = vol_response.json()
        prix = vol_data[0]['prix']
        return prix

    async def get_banque_info(username, numvol, rib, prix):
        """Récupère les informations de la banque associées à l'utilisateur.
        
        Args:
            username (str): Le nom d'utilisateur associé à la réponse.
            numvol (int): Le numéro de vol associé à la réponse.
            rib (int): Le RIB associé à la réponse.
            prix (int): Le prix associé à la réponse."""
        banque_response = requests.get(f"http://172.21.0.8:8001/users/rib/banque/?rib={rib}")
        banque_data = banque_response.json()
        id_rib = banque_data[0]['id']
        argent = banque_data[0]['argent']
        
        response_data = await manage_response(username, numvol, rib, argent, prix, id_rib)
        return response_data

    async def manage_response(username, numvol, rib, argent, prix, id_rib):
        """Gère la réponse de la banque.
        
        Args:
            username (str): Le nom d'utilisateur associé à la réponse.
            numvol (int): Le numéro de vol associé à la réponse.
            rib (int): Le RIB associé à la réponse.
            argent (int): L'argent associé à la réponse.
            prix (int): Le prix associé à la réponse."""
        if argent > prix:
            print(argent, prix)
            argent-= prix
            response = requests.put(f"http://172.21.0.8:8001/users/infos/banque/{id_rib}/", 
                                    data=f'{{"argent": {argent}}}', 
                                    headers={'Content-Type': 'application/json'})
            response_data = {"status": "True", "argent": argent, "username": username}
        else:
            response_data = {"status": "False"}
        return response_data

    data = json.loads(msg.data.decode())
    username = data['username']
    numvol = data['numvol']

    rib = await get_rib(username)
    prix = await get_vol_info(numvol)
    response_data = await get_banque_info(username, numvol, rib, prix)
    return response_data

async def run_subscriber():
    """Exécute le serveur NATS."""
    nc = await nats.connect("nats://172.21.0.10:4222")

    await nc.subscribe("banque.*", cb=message_handler)

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        await nc.close()

if __name__ == '__main__':
    path = os.path.join(os.path.dirname(__file__), 'hotline.json')
    asyncio.run(run_subscriber())