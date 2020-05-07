import random
import settings

def randomciv():
    pldic = {}
    pllist = []
    for name in settings.players:
        for i in range(3):
            pllist.append(part.pop(random.randint(0, len(part)-1)))
        pldic.setdefault(name, pllist)
        pllist = []
    return pldic
