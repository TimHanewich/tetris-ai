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

tai = TetrisAI()
gs = tetris.GameState()
p = tetris.Piece()
p.randomize()

v = tai.choose_move(p, gs)