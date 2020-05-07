import random
import settings

def randomciv():
    pldic = {}
    pllist = []
    for name in settings.players:
        for i in range(3):
            pllist.append(settings.part.pop(random.choice(settings.part)))
        pldic.setdefault(name, pllist)
        pllist = []
    return pldic
