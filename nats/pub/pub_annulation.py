import asyncio
import nats
import json
import os
import random

class PublishAnnulationValidation():
    """Classe pour publier des informations de validation d'annulation.
    
    Cette classe permet de publier des informations de validation d'annulation telles que le numéro de vol, l'annulation
    
    Attributes:
        numvol (int): Le numéro de vol associé aux informations de validation d'annulation.
        annulation (str): L'annulation associée aux informations de validation d'annulation.
        username (str): Le nom d'utilisateur associé aux informations de validation d'annulation."""
    def __init__(self, numvol = 1515199652, annulation = "True", username = "janedoe") -> None:
        """Initialise une instance de PublishAnnulationValidation.
        
        Args:
            numvol (int): Le numéro de vol associé aux informations de validation d'annulation.
            annulation (str): L'annulation associée aux informations de validation d'annulation.
            username (str): Le nom d'utilisateur associé aux informations de validation d'annulation."""
        self.numvol = numvol
        self.annulation = annulation
        self.username = username

    def setup(self):
        """Configure la publication des informations de validation d'annulation."""
        return asyncio.run(self.run_publisher())

    async def run_publisher(self):
        """Exécute la publication des informations de validation d'annulation."""
        nc = await nats.connect("nats://192.168.1.101:4222")

        data = json.dumps({"numvol": self.numvol, "annulation": self.annulation, "username": self.username})
        try:
            response = await nc.request("annulation.validation", data.encode(), timeout=5)  # Increase the timeout value here (in seconds)
        except KeyboardInterrupt:
            pass
        finally:
            await nc.close()
            return response.data.decode()

if __name__ == '__main__':
    print(PublishAnnulationValidation().setup())
