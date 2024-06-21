import asyncio
import nats
import json
import os
import random
from pub_bancaire import PublishBank
from pub_dispo import PublishDispo

def publish_reservation(numvol = 1515199652, username = "johndoe"):
    data = PublishBank(username, numvol).setup()
    data = json.loads(data)
    if data["status"] == "True":
        rep = PublishDispo(numvol = numvol, username=data["username"], argent=data["argent"]).setup()
        print(rep)

