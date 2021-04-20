from game.defines import *
import time
def CountToPostion(index, size):
    i = index // size
    j = index % size
    return i, j

def log(moudle_name):
    def log_(func):
        def wrapper(*args, **kargs):
            print("Execute {}.{}.".format(moudle_name, func.__name__))
            res = func(*args, **kargs)
            return res
        return wrapper
    return log_


def timer(func):
    def wrapper(*args, **kargs):
        global DEBUG
        t = time.time()
        res = func(*args, **kargs)
        if DEBUG_MODE:print("[Timer analyze] {} cost {}s.".format(func.__name__, time.time() - t))
        return res
    return wrapper

