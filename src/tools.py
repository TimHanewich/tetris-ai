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

def convert_seconds(seconds) -> tuple[int, int, int]:
    """Converts a number of elapsed seconds into an Hour, Minute, Second interval."""
    hours = seconds // 3600 
    minutes = (seconds % 3600) // 60 
    seconds = seconds % 60 
    return hours, minutes, seconds