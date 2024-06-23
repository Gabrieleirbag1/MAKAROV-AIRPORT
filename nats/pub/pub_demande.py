import asyncio
import nats
import json
import os
import random

class PublishAnnulationDemande():
    """Classe pour publier des informations de demande d'annulation.
    
    Attributes:
        numvol (int): Le numéro de vol associé aux informations de demande d'annulation.
        demande (str): La demande associée aux informations de demande d'annulation.
        username (str): Le nom d'utilisateur associé aux informations de demande d'annulation."""
    def __init__(self, numvol = 1515199652, demande = "True", username = "janedoe") -> None:
        """Initialise une instance de PublishAnnulationDemande.
        
        Args:
            numvol (int): Le numéro de vol associé aux informations de demande d'annulation.
            demande (str): La demande associée aux informations de demande d'annulation.
            username (str): Le nom d'utilisateur associé aux informations de demande d'annulation."""
        self.numvol = numvol
        self.demande = demande
        self.username = username

    def setup(self):
        """Configure la publication des informations de demande d'annulation."""
        return asyncio.run(self.run_publisher())

    async def run_publisher(self):
        """Exécute la publication des informations de demande d'annulation."""
        nc = await nats.connect("nats://192.168.1.57:4222")

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
