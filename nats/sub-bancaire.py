import asyncio
import nats
import json
import os
import requests

async def message_handler(msg):
    if msg.subject == "banque.*":
        response_data = await banque(msg)
    else:
        response_data = {"status": "ignore"}
    print("reponse", response_data)
    await msg.respond(json.dumps(response_data).encode())

async def banque(msg):
    async def get_vol_info(numvol):
        vol_response = requests.get(f"http://localhost:8001/vols/infos/?numvol={numvol}")
        vol_data = vol_response.json()
        prix = vol_data[0]['prix']
        print("prix", prix)
        return prix

    async def get_banque_info(rib, prix):
        print("rib", rib)
        banque_response = requests.get(f"http://localhost:8000/users/infos/banque/?rib={rib}")
        banque_data = banque_response.json()
        print(banque_data)
        argent = banque_data[0]['argent']
        
        response_data = await manage_response(rib, argent, prix)
        return response_data

    async def manage_response(rib, argent, prix):
        if argent > prix:
            print(argent, prix)
            argent-= prix
            response = requests.put(f"http://localhost:8000/users/infos/banque/?rib={rib}/", 
                                    data=f'{{"argent": {argent}}}', 
                                    headers={'Content-Type': 'application/json'})
            response_data = "True"
        else:
            response_data = "False"
        return response_data

    data = json.loads(msg.data.decode())
    rib = data['rib']
    numvol = data['numvol']

    prix = await get_vol_info(numvol)
    response_data = await get_banque_info(rib, prix)
    return response_data

async def run_subscriber():
    nc = await nats.connect("nats://127.0.0.1:4222")

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