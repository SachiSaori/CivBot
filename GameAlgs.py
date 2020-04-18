import random


def randomciv(players, part):
    pldic = {}
    pllist = []
    for name in players:
        for i in range(3):
            pllist.append(part.pop(random.choice(part)))
        pldic.setdefault(name, pllist)
        pllist = []
    return pldic
