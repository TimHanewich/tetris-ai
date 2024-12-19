print("Importing dependencies...")
import keras
import random
import numpy
import tetris
import representation

class PlayedGame:
    def __init__(self):
        self.piece_states:list[int] = [] # a list of all piece states we ran into
        self.board_states:list[int] = [] # a list of all board states we ran into
        self.decisions:list[int] = [] # a list of all decisions made
        self.final_score:int = 0 # the final score of the game after it was over

class TetrisAI:

    def __init__(self):

        # build NN v2

        # build input piece portion, followed by some hidden layers
        input_piece = keras.layers.Input(shape=(4,))
        carry_piece = keras.layers.Dense(16, "relu")(input_piece)
        carry_piece = keras.layers.Dense(16, "relu")(carry_piece)
        carry_piece = keras.layers.Dense(16, "relu")(carry_piece)
        carry_piece = keras.layers.Dense(16, "relu")(carry_piece)

        # build input board portion, followed by some layers
        input_board = keras.layers.Input(shape=(32,))
        carry_board = keras.layers.Dense(128, "relu")(input_board)
        carry_board = keras.layers.Dense(128, "relu")(carry_board)
        carry_board = keras.layers.Dense(128, "relu")(carry_board)
        carry_board = keras.layers.Dense(128, "relu")(carry_board)

        # combine the two into one layer, followed by some layers
        combined = keras.layers.concatenate([carry_piece, carry_board])
        carry = keras.layers.Dense(256, "relu")(combined)
        carry = keras.layers.Dense(256, "relu")(carry)
        carry = keras.layers.Dense(256, "relu")(carry)
        carry = keras.layers.Dense(256, "relu")(carry)
        output = keras.layers.Dense(4, "softmax")(carry)

        # construct the model
        self.model = keras.Model(inputs=[input_piece, input_board], outputs=output)
        self.model.compile("adam", "categorical_crossentropy") # use categorical_crossentropy because this is a classification problem (we are having it select from a set of options)

    def choose_move(self, p:tetris.Piece, gs:tetris.GameState) -> int:
        """Uses the neural network to choose the next move, returned as a shift between 0 and 3"""

        inputs_piece:list[int] = representation.PieceState(p)
        inputs_board:list[int] = representation.BoardState(gs)

        x1 = numpy.array([inputs_piece])
        x2 = numpy.array([inputs_board])

        prediction = self.model.predict([x1,x2])
        vals:list[float] = prediction[0]
        return int(numpy.argmax(vals))

    def train(self, games:list[PlayedGame], epochs:int) -> None:
        """Trains the neural network on a series of games that were deemed to be of relative success."""

        # assemble big list of inputs and outputs
        # x1_train:list[list[int]] = [] # piece inputs
        # x2_train:list[list[int]] = [] # board inputs
        # y_train:list[list[int]] = [] # the "correct decision" outputs
        # for game in games:
        #     x1_train.extend()
        
        # assemble the big list of inputs and outputs
        x_train:list[list[int]] = []
        y_train:list[list[int]] = []
        for game in games:
            x_train.extend(game.states)
            y_train.extend(game.decisions)

        # convert to numpy arrays
        x_train = numpy.array(x_train)
        y_train = numpy.array(y_train)

        # train
        self.model.fit(x_train, y_train, epochs=epochs)
    
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
        shift:int = tai.choose_move(p, gs)

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

# construct model
print("Constructing model...")
tai = TetrisAI()  

# settings for training
games_in_batch:int = 200 # how many games will be played (simulated), with the top X% being used to train
best_game_focus:int = 20 # the top X games that will be trained on
accrue_games_before_training:int = 1000 # the number of TOP games (games that will be trained on) which will be collected before it trains on them
training_epochs:int = 30 # the number of epochs those accrued good games are trained on
total_games:int = 100000 # the total number of games to train on. Once the model has been trained on this number, it will stop
save_checkpoint_every_trained:int = 1000 # after training each X number of games, a checkpoint will be saved

# numbers to track
games_trained:int = 0
on_checkpoint:int = 0
games_trained_at_last_checkpoint:int = 0

# train!
while games_trained < total_games:

    GamesToTrainOn:list[PlayedGame] = [] # the top games that we will train on later
    avg_score:float = 0.0 # will be reported on during training so user watching can track progress
    while len(GamesToTrainOn) < accrue_games_before_training:

        status:str = "(" + str(games_trained) + " trained / " + str(total_games) + " goal) (" + str(len(GamesToTrainOn)) + " accrued / " + str(accrue_games_before_training) + " batch goal) (" + str(round(avg_score, 1)) + " avg score)"

        # play (simulate) games
        GameSimulations:list[PlayedGame] = []
        for x in range(0, games_in_batch):
            print(status + " " + "Simulating game # " + str(x) + " / " + str(games_in_batch))
            pg = simulate_game(tai)
            GameSimulations.append(pg)

        # get avg score
        score:int = 0
        for pg in GameSimulations:
            score = score + pg.final_score
        avg_score = score / len(GameSimulations)
        print("Avg score of this group of " + str(len(GameSimulations)) + " simulations: " + str(avg_score))

        # sort by score
        print("Sorting " + str(len(GameSimulations)) + " games by score...")
        GameSimulationsOrdered:list[PlayedGame] = []
        while len(GameSimulations) > 0:
            best:PlayedGame = GameSimulations[0]
            for pg in GameSimulations:
                if pg.final_score > best.final_score:
                    best = pg
            GameSimulationsOrdered.append(best)
            GameSimulations.remove(best)

        # take the top X games and store them
        print("Selecting best " + str(best_game_focus) + " games for future training...")
        for i in range(best_game_focus): # take the top ones
            GamesToTrainOn.append(GameSimulationsOrdered[i])
    
    # we now have enough games accrued to start training, train now!
    print(str(len(GamesToTrainOn)) + " games reached. Entering training phase...")
    tai.train(GamesToTrainOn, training_epochs)
    games_trained = games_trained + len(GamesToTrainOn)
    print("Training complete! Total games trained now @ " + str(games_trained) + " out of goal of " + str(total_games) + ".")

    # is it time to save a checkpoint?
    if (games_trained - games_trained_at_last_checkpoint) >= save_checkpoint_every_trained: # it is time to save a checkpoint
        path:str = r"C:\Users\timh\Downloads\tah\tetris-ai\checkpoints\checkpoint" + str(on_checkpoint) + ".keras"
        tai.model.save(path)
        print("Checkpoint # " + str(on_checkpoint) + " saved to " + path + "!")
        on_checkpoint = on_checkpoint + 1
        games_trained_at_last_checkpoint = games_trained
