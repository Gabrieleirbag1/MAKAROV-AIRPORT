import asyncio
import nats
import json
import os
import requests
import threading

class SubscriberDispo():
    def __init__(self) -> None:
        self.nc = None

    def setup(self):
        return asyncio.run(self.run_subscriber())

    async def message_handler(self, msg):
        if msg.subject == f"dispo.*":
            response_data = await self.dispo(msg)
        else:
            response_data = {"status": "ignore"}
        print("reponse", response_data)
        await msg.respond(json.dumps(response_data).encode())

    async def dispo(self, msg):
        async def get_avion(numvol):
            print(numvol)
            url = f"http://172.21.0.2:8002/vols/infos/?numvol={numvol}"
            headers = {"Content-Type": "application/json"}
            response = requests.get(url, headers=headers)
            response_data = response.json()
            avion = response_data[0]["avion_ref"]
            return avion
        
        async def get_dispo(avion):
            url = f"http://172.21.0.4:8004/structure/infos/avions/?modele={avion}"
            headers = {"Content-Type": "application/json"}
            response = requests.get(url, headers=headers)
            response_data = response.json()
            dispo = response_data[0]["places"]
            return dispo
        
        async def get_nb_reservations(numvol):
            url = f"http://172.21.0.3:8003/reservations/infos/"
            headers = {"Content-Type": "application/json"}
            response = requests.get(url, headers=headers)
            response_data = response.json()
            nb_reservations = sum(1 for reservation in response_data if reservation['vol_ref'] == numvol and reservation['annulation'] == False)
            return nb_reservations

        data = json.loads(msg.data.decode())
        numvol = data['numvol']
        self.username = data['username']
        self.argent = data['argent']
        avion = await get_avion(numvol)
        dispo = await get_dispo(avion)
        nb_reservations = await get_nb_reservations(numvol)
        
        print(f"Avion: {avion}")
        print(f"Dispo: {dispo}")
        print(f"Reservations: {nb_reservations}")

        if nb_reservations < dispo:
            data = {
                'vol_ref': f"{numvol}",
                'user_ref': self.username,
                'demande': 'False',
                'annulation': 'False'
            }
            response = requests.post(f"http://172.21.0.3:8003/reservations/infos/",
                                    data=json.dumps(data),
                                    headers={'Content-Type': 'application/json'})
            print(response.json()["user_ref"])
            if "user ref already exists" in response.json()["user_ref"]:
                return {"status": "False"}
            
            return {"status": "True"} | response.json()

        return {"status": "False"}

    async def run_subscriber(self):
        self.nc = await nats.connect("nats://172.21.0.10:4222")

        await self.nc.subscribe(f"dispo.*", cb=self.message_handler)

        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            await self.nc.close()

if __name__ == '__main__':
    ui = SubscriberDispo().setup()