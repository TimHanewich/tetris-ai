def log(path:str, content:str) -> None:
    f = open(path, "a")
    f.write(content + "\n")
    f.close()