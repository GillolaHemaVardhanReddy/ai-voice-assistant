def greet():
    return "hi"


def loud(fn):
    def wrapper():
        return fn().upper() + "!!!"
    return wrapper

x = loud(greet)
print(x())