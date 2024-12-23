import random

def log(path:str, content:str) -> None:
    if path != None and path != "":
        f = open(path, "a")
        f.write(content + "\n")
        f.close()

def oddsof(odds:float) -> bool:
    return random.random() < odds

def highest_index(data:list[float]) -> int:
    """Returns the index of the highest floating point number in the list."""
    return data.index(max(data))