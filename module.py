def getMove(val)->tuple:
    switcher = {
        "w": (0, -1),
        "a": (-1, 0),
        "s": (0, 1),
        "d": (1, 0)
    }

    return switcher.get(val, (0, 0))

def loopVal(val, max)->int:
    if(val == -1):
        return max
    elif(val == max):
        return 0
    return val