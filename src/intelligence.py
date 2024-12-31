import keras
import numpy
import tetris
import random
import representation

class Experience:
    def __init__(self):
        self.state:tuple[list[int], list[int]] = None # the "state" the AI has seen. The first list is the state of the piece while the second list is the state of the board.
        self.action:int = None # the action the AI decided to take (the number of shifts it played).
        self.reward:float = None # the immediate reward (or we would call it penalty if it is negative) that the game gave to the AI for choosing it's action.
        self.next_state:tuple[list[int], list[int]] = None # same as the state variable above, but represents the RESULTING state that the AI finds itself in in this game after the action took place. This will be important for determining an estimate for "future rewards"
        self.done:bool = False # marks if the game is complete or not after this action was taken. This is important becuase, if the game is OVER, there is no need to consider potential future rewards... there won't be any potential future rewards! So just consider the immediate reward and take it!

class TetrisAI:

    def __init__(self, save_file_path:str = None):

        # if there is a save_file_path provided, load that
        if save_file_path != None:
            self.model = keras.models.load_model(save_file_path) # load from file path
        else:

            # build input piece portion, followed by some hidden layers
            input_piece = keras.layers.Input(shape=(8,), name="input_piece")
            carry_piece = keras.layers.Dense(32, "relu", name="piece_layer1")(input_piece)
            carry_piece = keras.layers.Dense(32, "relu", name="piece_layer2")(carry_piece)
            carry_piece = keras.layers.Dense(32, "relu", name="piece_layer3")(carry_piece)

            # build input board portion, followed by some layers
            input_board = keras.layers.Input(shape=(10,), name="input_board")
            carry_board = keras.layers.Dense(40, "relu", name="board_layer1")(input_board)
            carry_board = keras.layers.Dense(40, "relu", name="board_layer2")(carry_board)
            carry_board = keras.layers.Dense(40, "relu", name="board_layer3")(carry_board)

            # combine the two into one layer, followed by some layers
            combined = keras.layers.concatenate([carry_piece, carry_board], name="combined")
            carry = keras.layers.Dense(256, "relu", name="combined_layer1")(combined)
            carry = keras.layers.Dense(256, "relu", name="combined_layer2")(carry)
            carry = keras.layers.Dense(128, "relu", name="combined_layer3")(carry)
            carry = keras.layers.Dense(128, "relu", name="combined_layer4")(carry)
            carry = keras.layers.Dense(64, "relu", name="combined_layer5")(carry)
            output = keras.layers.Dense(9, "linear", name="output")(carry) # output of 9 potential moves (shift of 0 to shift of 9)

            # construct the model
            self.model = keras.Model(inputs=[input_piece, input_board], outputs=output)
            self.model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001), loss="mse")

    def save(self, path:str) -> None:
        """Saves the keras model to file"""
        self.model.save(path)

    def predict(self, piece:list[int], board:list[int]) -> list[float]:
        """Performs a forward pass through the neural net to predict the Q-values (current/future rewards) of each potential next move (shift) given the current state, returning as an array of floating point numbers."""
        x1 = numpy.array([piece])
        x2 = numpy.array([board])
        prediction = self.model.predict([x1,x2], verbose=False)
        vals:list[float] = prediction[0].tolist() # the "tolist()" function just converts it from a numpy.darray to a normal list of floats!
        return vals
    
    def train(self, state_piece:list[int], state_board:list[int], qvalues:list[float]) -> None:
        """Trains the model on the given 'correct' outputs, or Q-Values. Think of the 'q-values' as the 'correct' outputs for this particular state, where the target reward has been updated given what we learned from a recent experience."""
        x1 = numpy.array([state_piece])
        x2 = numpy.array([state_board])
        y = numpy.array([qvalues])
        self.model.fit([x1,x2], y, epochs=1, verbose=0)