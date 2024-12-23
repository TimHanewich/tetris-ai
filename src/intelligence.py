import keras
import numpy
import tetris
import random
import representation

class TetrisAI:

    def __init__(self, save_file_path:str = None):

        # if there is a save_file_path provided, load that
        if save_file_path != None:
            self.model = keras.models.load_model(save_file_path) # load from file path
        else:

            # build input piece portion, followed by some hidden layers
            input_piece = keras.layers.Input(shape=(8,), name="input_piece")
            carry_piece = keras.layers.Dense(32, "relu", name="piece_layer1")(input_piece)
            carry_piece = keras.layers.Dense(16, "relu", name="piece_layer2")(carry_piece)
            carry_piece = keras.layers.Dense(8, "relu", name="piece_layer3")(carry_piece)

            # build input board portion, followed by some layers
            input_board = keras.layers.Input(shape=(10,), name="input_board")
            carry_board = keras.layers.Dense(100, "relu", name="board_layer1")(input_board)
            carry_board = keras.layers.Dense(75, "relu", name="board_layer2")(carry_board)
            carry_board = keras.layers.Dense(50, "relu", name="board_layer3")(carry_board)

            # combine the two into one layer, followed by some layers
            combined = keras.layers.concatenate([carry_piece, carry_board], name="combined")
            carry = keras.layers.Dense(120, "relu", name="combined_layer1")(combined)
            carry = keras.layers.Dense(80, "relu", name="combined_layer2")(carry)
            carry = keras.layers.Dense(50, "relu", name="combined_layer3")(carry)
            carry = keras.layers.Dense(30, "relu", name="combined_layer4")(carry)
            output = keras.layers.Dense(9, "softmax", name="output")(carry) # output of 9 potential moves (shift of 0 to shift of 9)

            # construct the model
            self.model = keras.Model(inputs=[input_piece, input_board], outputs=output)
            self.model.compile("adam", "categorical_crossentropy") # use categorical_crossentropy because this is a classification problem (we are having it select from a set of options)

    def save(self, path:str) -> None:
        """Saves the keras model to file"""
        self.model.save(path)