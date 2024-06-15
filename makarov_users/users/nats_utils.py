import asyncio
import nats
import json
import os
import random

class PublishBank():
    def __init__(self, rib=41672307, num_vol=353629857) -> None:
        self.rib = rib
        self.num_vol = num_vol
        asyncio.run(self.run_publisher())

    async def run_publisher(self):
        nc = await nats.connect("nats://127.0.0.1:4222")
        data = json.dumps({"num_vol": self.num_vol, "rib": self.rib})
        try:
            response = await nc.request("banque.*", data.encode())
            print(response.data.decode())
        except KeyboardInterrupt:
            pass
        finally:
            await nc.close()

if __name__ == '__main__':
    PublishBank()