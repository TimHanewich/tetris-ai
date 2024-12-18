import keras
import random
import numpy
import tetris
import representation

class TetrisAI:

    def __init__(self):

        # build neural network
        self.model = keras.Sequential()
        self.model.add(keras.layers.Input(shape=(36,))) # inputs
        self.model.add(keras.layers.Dense(300, "relu"))
        self.model.add(keras.layers.Dense(250, "relu"))
        self.model.add(keras.layers.Dense(200, "relu"))
        self.model.add(keras.layers.Dense(150, "relu"))
        self.model.add(keras.layers.Dense(100, "relu"))
        self.model.add(keras.layers.Dense(50, "relu"))
        self.model.add(keras.layers.Dense(25, "relu"))
        self.model.add(keras.layers.Dense(4)) # outputs 
        self.model.compile("adam", "mean_squared_error")


    def choose_move(self, p:tetris.Piece, gs:tetris.GameState) -> int:
        """Uses the neural network to choose the next move, returned as a shift between 0 and 3"""

        inputs:list[int] = representation.StateInputs(p, gs) # convert new piece and game state as representation of ints
        ninputs = numpy.array([inputs]) # load into a numpy array
        outputs = self.model.predict(ninputs, verbose=False)
        
        vals:list[float] = outputs[0]
        print(vals)
        return int(numpy.argmax(vals))

class PlayedGame:
    def __init__(self):
        self.states:list[int] = [] # a list of all states evaluated
        self.decisions:list[int] = [] # a list of all decisions made
        self.final_score:int = 0 # the final score of the game after it was over

def simulate_game(tai:TetrisAI) -> PlayedGame:
    gs:tetris.GameState = tetris.GameState()

    while True:

        # generate random piece
        p:tetris.Piece = tetris.Piece()
        p.randomize()

        # ask the NN to play the next game
        shift:int = tai.choose_move(p, gs)