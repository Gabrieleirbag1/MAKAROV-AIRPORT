import asyncio
import nats
import json
import os
import random

class PublishBank():
    def __init__(self, rib = 41672307, numvol = 353629857) -> None:
        self.rib = rib
        self.numvol = numvol

    def setup(self):
        return asyncio.run(self.run_publisher())

    async def run_publisher(self):
        nc = await nats.connect("nats://127.0.0.1:4222")

        data = json.dumps({"numvol": self.numvol, "rib": self.rib})
        try:
            response = await nc.request("banque.*", data.encode())
        except KeyboardInterrupt:
            pass
        finally:
            await nc.close()
            return response.data.decode()

if __name__ == '__main__':
    print(PublishBank().setup())