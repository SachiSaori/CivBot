import random


def randomciv(players, part):
    pldic = {}
    pllist = []
    for name in players:
        for i in range(3):
            pllist.append(part.pop(random.randint(0, len(part)-1)))
        pldic.setdefault(name, pllist)
        pllist = []
    return pldic
