import tetris

while True:
    gs = tetris.GameState()
    
    while True:
        p = tetris.Piece()
        p.randomize()
        print("Piece:")
        print(str(p))

        print("Board:")
        print(str(gs))

        i:str = input("How many shifts? > ")
        shifts:int = int(i)
        reward:float = gs.drop(p, shifts)
        print("Reward from move '" + str(round(reward, 1)) + "'")

        # if game over
        if gs.over():
            print("Game over!")
            print("Score: " + str(gs.score()))
            input("Enter to go to next game.")
            gs = tetris.GameState()
