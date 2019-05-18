import random


def autoban(civils):
    for i in range(3):
        civils.pop(random.randint(0, len(civils)))
    return civils


def randomciv(players, part):
    pldic = {}
    pllist = []
    for name in players:
        for i in range(3):
            pllist.append(part.pop(random.randint(0, len(part)-1)))
        pldic.setdefault(name, pllist)
        pllist = []
    return pldic
