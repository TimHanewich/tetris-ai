import tetris
import random
import copy

gs = tetris.GameState()

while True:

    p = tetris.Piece()
    p.randomize()

    # select highest move
    best_move:int = 0
    best_move_reward:float = 0.0
    for i in range(0, 9):
        gst = tetris.GameState()
        gst.board = copy.deepcopy(gs.board)
        try:
            reward:float = gst.drop(p, i)
            if reward > best_move_reward:
                best_move = i
                best_move_reward = reward
        except Exception as ex:
            pass


    # execute best move
    reward:float = gs.drop(p, best_move)
    print("Reward from move: " + str(round(reward, 2)))

    # print
    print(str(gs))
    input("-------")

    # new game?
    if gs.over():
        gs = tetris.GameState()