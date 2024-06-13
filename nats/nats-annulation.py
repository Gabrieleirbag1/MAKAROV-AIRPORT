import asyncio
import nats
import requests
import json

async def run_publisher():
    nc = await nats.connect("nats://127.0.0.1:4222")

    async def message_handler(msg):
        request = json.loads(msg.data.decode())
        response = requests.post('http://localhost:8000/sncf_app/infos/', data=request)
        print(f"Response status: {response.status_code}")

    await nc.subscribe("infoClient.create", cb=message_handler)

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        await nc.close()

if __name__ == '__main__':
    asyncio.run(run_publisher())