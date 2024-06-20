import asyncio
import nats
import json
import os
import random

class PublishAnnulationDemande():
    def __init__(self, numvol = 353629857, demande = "True", username = "janedoe") -> None:
        self.numvol = numvol
        self.demande = demande
        self.username = username

    def setup(self):
        return asyncio.run(self.run_publisher())

    async def run_publisher(self):
        nc = await nats.connect("nats://127.0.0.1:4222")

        data = json.dumps({"numvol": self.numvol, "demande": self.demande, "username": self.username})
        try:
            response = await nc.request("annulation.demande", data.encode(), timeout=5)  # Increase the timeout value here (in seconds)
        except KeyboardInterrupt:
            pass
        finally:
            await nc.close()
            return response.data.decode()

if __name__ == '__main__':
    print(PublishAnnulationDemande().setup())
