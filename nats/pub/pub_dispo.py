import asyncio
import nats
import json
import os
import random

class PublishDispo():
    """Classe pour publier des informations de disponibilité.
    
    Cette classe permet de publier des informations de disponibilité telles que le numéro de vol et l'annulation associée.
    
    Attributs:
        numvol (int): Le numéro de vol associé aux informations de disponibilité."""
    def __init__(self, numvol = 1515199652, username = "johndoe", argent = 1000) -> None:
        """Initialise une instance de PublishDispo."""
        self.numvol = numvol
        self.username = username
        self.argent = argent

    def setup(self):
        """Configure la publication des informations de disponibilité."""
        return asyncio.run(self.run_publisher())

    async def run_publisher(self):
        """Exécute la publication des informations de disponibilité."""
        nc = await nats.connect("nats://192.168.1.57:4222")

        data = json.dumps({"numvol": self.numvol, "username": self.username, "argent": self.argent})
        try:
            response = await nc.request("dispo.*", data.encode(), timeout=5)  # Augmentez la valeur du délai d'attente ici (en secondes)
        except KeyboardInterrupt:
            pass
        finally:
            await nc.close()
            return response.data.decode()

if __name__ == '__main__':
    print(PublishDispo().setup())
