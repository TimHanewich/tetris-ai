import keras
import numpy
import tetris
import random
import representation

class PlayedGame:
    def __init__(self):
        self.piece_states:list[int] = [] # a list of all piece states we ran into
        self.board_states:list[int] = [] # a list of all board states we ran into
        self.decisions:list[int] = [] # a list of all decisions made
        self.final_score:int = 0 # the final score of the game after it was over

class TetrisAI:

    def __init__(self, save_file_path:str = None):

        # if there is a save_file_path provided, load that
        if save_file_path != None:
            self.model = keras.models.load_model(save_file_path) # load from file path
        else:

            # build input piece portion, followed by some hidden layers
            input_piece = keras.layers.Input(shape=(4,), name="input_piece")
            carry_piece = keras.layers.Dense(16, "relu", name="piece_layer1")(input_piece)
            carry_piece = keras.layers.Dense(16, "relu", name="piece_layer2")(carry_piece)
            carry_piece = keras.layers.Dense(16, "relu", name="piece_layer3")(carry_piece)
            carry_piece = keras.layers.Dense(16, "relu", name="piece_layer4")(carry_piece)

            # build input board portion, followed by some layers
            input_board = keras.layers.Input(shape=(4,), name="input_board")
            carry_board = keras.layers.Dense(64, "relu", name="board_layer1")(input_board)
            carry_board = keras.layers.Dense(64, "relu", name="board_layer2")(carry_board)
            carry_board = keras.layers.Dense(64, "relu", name="board_layer3")(carry_board)
            carry_board = keras.layers.Dense(64, "relu", name="board_layer4")(carry_board)

            # combine the two into one layer, followed by some layers
            combined = keras.layers.concatenate([carry_piece, carry_board], name="combined")
            carry = keras.layers.Dense(256, "relu", name="combined_layer1")(combined)
            carry = keras.layers.Dense(256, "relu", name="combined_layer2")(carry)
            carry = keras.layers.Dense(128, "relu", name="combined_layer3")(carry)
            carry = keras.layers.Dense(128, "relu", name="combined_layer4")(carry)
            carry = keras.layers.Dense(64, "relu", name="combined_layer5")(carry)
            output = keras.layers.Dense(4, "softmax", name="output")(carry)

            # construct the model
            self.model = keras.Model(inputs=[input_piece, input_board], outputs=output)
            self.model.compile("adam", "categorical_crossentropy") # use categorical_crossentropy because this is a classification problem (we are having it select from a set of options)

    def choose_move(self, p:tetris.Piece, gs:tetris.GameState, random_exploration:bool) -> int:
        """Uses the neural network to choose the next move, returned as a shift between 0 and 3. If `random_exploration` is True, will sometimes (infrequently) choose a random move, encouraging exploration."""

        # determine if we should select random or choose move normally using the neural network
        # (the select random option is there for exploration)
        SelectRandom:bool = False
        if random_exploration:
            if (oddsof(0.10)): # % of the time it should select a random move
                SelectRandom = True
        
        # handle if we should select random or actually decide what to do using the NN
        if SelectRandom: # if it was determined we should play a random move (explore), play a random move. But play a legal move that does not invalidate the game!
            RandomMoveToReturn:int = 0
            if p.width == 2: # if the width is 2, that means a shift of 3 would not work (part of the piece would be hanging off the board, an illegal move). So only consider the moves 0, 1, and 2.
                RandomMoveToReturn:int = random.randint(0, 2)
            else:
                RandomMoveToReturn:int = random.randint(0, 3)
            return RandomMoveToReturn
        else: # if it was not determined we should play a random move, select normally
            inputs_piece:list[int] = representation.PieceState(p)
            inputs_board:list[int] = representation.BoardState(gs)

            x1 = numpy.array([inputs_piece])
            x2 = numpy.array([inputs_board])

            prediction = self.model.predict([x1,x2], verbose=False)
            vals:list[float] = prediction[0]
            SelectedMove:int = int(numpy.argmax(vals))
            return SelectedMove

    def train(self, games:list[PlayedGame], epochs:int) -> None:
        """Trains the neural network on a series of games that were deemed to be of relative success."""

        # assemble big list of inputs and outputs
        x1_train:list[list[int]] = [] # piece inputs
        x2_train:list[list[int]] = [] # board inputs
        y_train:list[list[int]] = [] # the "correct decision" outputs
        for game in games:
            x1_train.extend(game.piece_states)
            x2_train.extend(game.board_states)
            y_train.extend(game.decisions)

        # convert to numpy arrays
        x1_train = numpy.array(x1_train)
        x2_train = numpy.array(x2_train)
        y_train = numpy.array(y_train)

        # train
        self.model.fit([x1_train,x2_train], y_train, epochs=epochs)

    def save(self, path:str) -> None:
        """Saves the keras model to file"""
        self.model.save(path)
    
def simulate_game(tai:TetrisAI) -> PlayedGame:
    ToReturn = PlayedGame()

    # simulate the game
    gs:tetris.GameState = tetris.GameState()
    while True:

        # generate random piece
        p:tetris.Piece = tetris.Piece()
        p.randomize()

        # before moving create the board state situation and piece state
        piece_state:list[int] = representation.PieceState(p)
        board_state:list[int] = representation.BoardState(gs)

        # ask the NN to deicde what the next move should be (decide where to drop the piece)
        shift:int = tai.choose_move(p, gs, True)

        # create the output representation of that move
        outputs:list[int] = [0,0,0,0]
        outputs[shift] = 1

        # log the input/output pair
        ToReturn.piece_states.append(piece_state) # add the piece we just dealt with
        ToReturn.board_states.append(board_state) # add the board we just dealt with
        ToReturn.decisions.append(outputs) # add the decision we just made

        # make the move
        try:
            gs.drop(p, shift)
        except tetris.InvalidShiftException as ex:

            # mark down the final score as 0
            ToReturn.final_score = 0

            # return
            return ToReturn
        except Exception as ex:
            print("Unhandled exception in move execution: " + str(ex))
            input("Waiting for next enter from you.")

        # if the game is now over, finish
        if gs.over():
            ToReturn.final_score = gs.score() # mark down final score
            return ToReturn
        
def oddsof(odds:float) -> bool:
    return random.random() < odds