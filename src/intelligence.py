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
        self.final_reward:int = 0 # the final reward of the game after it was over

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

    def choose_move(self, p:tetris.Piece, gs:tetris.GameState, epsilon:float = 0.0) -> int:
        """Uses the neural network to choose the next move, returned as a shift between 0 and 3. 'epsilon' sets the e-greedy value. At 100% (1.0), it will choose a random legal move every time. At 0%, it will choose the move that it believe is best every time. Higher epsilon encourages exploration."""
        
        # handle if we should select random or actually decide what to do using the NN
        if oddsof(epsilon): # if it was determined we should play a random move (explore), play a random move. But play a legal move that does not invalidate the game!
            RandomMoveToReturn:int = 0
            if p.width == 2:
                RandomMoveToReturn = random.randint(0, 8)
            elif p.width == 3: # most pieces
                RandomMoveToReturn = random.randint(0, 7)
            elif p.width == 4:
                RandomMoveToReturn = random.randint(0, 6)
            else:
                raise Exception("Potential legal moves not known for piece with width '" + str(p.width) + "'.")
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
    
def simulate_game(tai:TetrisAI, epsilon:float = 0.0) -> PlayedGame:
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
        shift:int = tai.choose_move(p, gs, epsilon)

        # create the output representation of that move
        outputs:list[int] = [0,0,0,0,0,0,0,0,0] # array of 9
        outputs[shift] = 1

        # log the input/output pair
        ToReturn.piece_states.append(piece_state) # add the piece we just dealt with
        ToReturn.board_states.append(board_state) # add the board we just dealt with
        ToReturn.decisions.append(outputs) # add the decision we just made

        # make the move
        try:
            gs.drop(p, shift)
        except tetris.InvalidShiftException as ex:            
            ToReturn.final_reward = 0 # mark down the final reward as 0 as punishment for playing an illegal move!
            return ToReturn # return
        except Exception as ex:
            print("Unhandled exception in move execution: " + str(ex))
            input("Waiting for next enter from you.")

        # if the game is now over, finish
        if gs.over():
            ToReturn.final_reward = gs.reward() # mark down the reward
            ToReturn.final_score = gs.score() # mark down the score
            return ToReturn