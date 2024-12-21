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

        i:str = input("How many shifts? (0-3) > ")
        shifts:int = int(i)
        gs.drop(p, shifts)

        # if game over
        if gs.over():
            print("Game over!")
            print("Score: " + str(gs.score))
            input("Enter to go to next game.")
