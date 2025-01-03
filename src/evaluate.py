import intelligence
import tetris
import representation

save_path = r""
tai = intelligence.TetrisAI(save_path)

while True:
    gs = tetris.GameState()
    gs.randomize(5)
    while True:
        p = tetris.Piece()
        p.randomize()

        print("Piece:")
        print(str(p))

        print("Board:")
        print(str(gs))

        # get move
        predictions:list[float] = tai.predict(representation.PieceState(p), representation.BoardState(gs))
        shift:int = predictions.index(max(predictions))
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

