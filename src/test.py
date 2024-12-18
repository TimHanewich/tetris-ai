from tetris import GameState, Piece
import representation
import random

gs:GameState = GameState()
while True:
    
    p:Piece = Piece()
    p.randomize()
    print("Piece:")
    print(str(p))

    print("Board before: ")
    print(gs)

    print("Inputs: " + str(representation.StateInputs(p, gs)))

    # move
    if p.columns_occupied() == 2:
        gs.drop(p, random.randint(0,2))
    else:
        gs.drop(p, random.randint(0,3))

    print("Board after: ")
    print(gs)

    if gs.over():
        print("Game is over with score " + str(gs.score()) + "! Game reset.")
        gs = GameState()

    input()