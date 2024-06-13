import asyncio
import nats
import json
import os

async def message_handler(msg):
    data = json.loads(msg.data.decode())
    if "chris" in data["code"]:
        response_data = {"status": "ok"}
    else:
        response_data = {"status": "not ok"}
    await msg.respond(json.dumps(response_data).encode())

async def run_subscriber():
    nc = await nats.connect("nats://127.0.0.1:4222")

    await nc.subscribe("hotline", cb=message_handler)

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