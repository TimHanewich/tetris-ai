import intelligence
import tetris

save_path = r""
tai = intelligence.TetrisAI(save_path)

while True:
    gs = tetris.GameState()
    while True:
        p = tetris.Piece()
        p.randomize()

        print("Piece:")
        print(str(p))

        print("Board:")
        print(str(gs))

        # get move
        shift:int = tai.choose_move(p, gs, 0.0)
        print("Move: " + str(shift))
        input("Enter to execute the move it selected")

        # make move
        gs.drop(p, shift)

        # if game over
        if gs.over():
            print("Game is over!")
            print("Final score: " + str(gs.score()))
            print("Going to next game...")
            gs = tetris.GameState()

