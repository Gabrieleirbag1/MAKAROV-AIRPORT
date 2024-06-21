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
        nc = await nats.connect("nats://127.0.0.1:4222")

        data = json.dumps({"numvol": self.numvol, "username": self.username, "argent": self.argent})
        try:
            response = await nc.request("dispo.*", data.encode(), timeout=5)  # Augmentez la valeur du délai d'attente ici (en secondes)
        except KeyboardInterrupt:
            pass
        finally:
            await nc.close()
            return response.data.decode()
        
class PublishBank():
    """Classe pour publier des informations bancaires.

    Cette classe permet de publier des informations bancaires telles que le numéro de vol et le nom d'utilisateur
    vers un serveur NATS.

    Attributes:
        username (str): Le nom d'utilisateur associé aux informations bancaires.
        numvol (int): Le numéro de vol associé aux informations bancaires.
    """

    def __init__(self, username="aedsdkhmvl", numvol=353629857) -> None:
        """Initialise une instance de PublishBank.
        
        Args:
            username (str): Le nom d'utilisateur associé aux informations bancaires.
            numvol (int): Le numéro de vol associé aux informations bancaires."""
        self.username = username
        self.numvol = numvol

    def setup(self):
        """Configure la publication des informations bancaires."""
        return asyncio.run(self.run_publisher())

    async def run_publisher(self):
        """Exécute la publication des informations bancaires."""
        nc = await nats.connect("nats://127.0.0.1:4222")

        data = json.dumps({"numvol": self.numvol, "username": self.username})
        try:
            response = await nc.request("banque.*", data.encode())
        except KeyboardInterrupt:
            pass
        finally:
            await nc.close()
            return response.data.decode()
        
def publish_reservation(numvol = 1515199652, username = "owen"):
    data = PublishBank(username, numvol).setup()
    data = json.loads(data)
    if data["status"] == "True":
        rep = PublishDispo(numvol = numvol, username=data["username"], argent=data["argent"]).setup()
        print(rep)
        return rep

if __name__ == '__main__':
    publish_reservation()

# -> return {"status": "True", "id": 7, "vol_ref": 353629857, "user_ref": "aedsdkhmvl", "demande": false, "annulation": false}
