def getMove(val)->tuple:
    switcher = {
        "W": (0, -1),
        "A": (-1, 0),
        "S": (0, 1),
        "D": (1, 0)
    }

    return switcher.get(val, (0, 0))

def loopVal(val)->int:
    if(val == -1):
        return 40
    elif(val == 40):
        return 0
    return val