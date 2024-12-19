print("Importing dependencies...")
import keras
import random
import numpy
import tetris
import representation

class PlayedGame:
    def __init__(self):
        self.states:list[int] = [] # a list of all states evaluated
        self.decisions:list[int] = [] # a list of all decisions made
        self.final_score:int = 0 # the final score of the game after it was over

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
        return int(numpy.argmax(vals))

    def train(self, games:list[PlayedGame], epochs:int) -> None:
        """Trains the neural network on a series of games that were deemed to be of relative success."""
        
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

        # create the input representation
        inputs:list[int] = representation.StateInputs(p, gs)

        # ask the NN to play the next game
        shift:int = tai.choose_move(p, gs)

        # create the output representation
        outputs:list[int] = [0,0,0,0]
        outputs[shift] = 1

        # log the input/output pair
        ToReturn.states.append(inputs)
        ToReturn.decisions.append(outputs)

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

        # if the game is over, finish
        if gs.over():
            ToReturn.final_score = gs.score() # mark down final score
            return ToReturn

# construct model
print("Constructing model...")
tai = TetrisAI()  

# settings for training
games_in_batch:int = 100 # how many games will be played (simulated), with the top X% being used to train
best_game_focus:int = 20 # the top X games that will be trained on
accrue_games_before_training:int = 20 # the number of TOP games (games that will be trained on) which will be collected before it trains on them
training_epochs:int = 50 # the number of epochs those accrued good games are trained on
total_games:int = 1000 # the total number of games to train on. Once the model has been trained on this number, it will stop

# numbers to track
games_trained:int = 0
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