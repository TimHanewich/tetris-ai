import intelligence
import sys
import tools
import tetris
import representation
import random
import time
import math

### SETTINGS ###
model_save_path = r"" # if you want to start from a checkpoint, fill this in with the path to the .keras file. If wanting to start from a new NN, leave blank!
log_file_path:str = r"C:\Users\timh\Downloads\tah\tetris-ai\checkpoints\log.txt" # during training, if you want logs to be saved in this file about the progress of performance improvemnts during training, put a path to a txt file here. Logs will be appended.

# training settings
gamma:float = 0.5
epsilon:float = 0.2

# training config
collect_experiences:int = 500 # how many moves the model will play (across multiple games) before stopping to train on those moves and their associated reward.
train_on_percent_of_experiences_batch:float = 0.25 # what percentage of the experiences will be trained on
################


# construct/load model
tai:intelligence.TetrisAI = None
if model_save_path != None and model_save_path != "":
    print("Loading model checkpoint at '" + model_save_path + "'...")
    tai = intelligence.TetrisAI(model_save_path)
    print("Model loaded!")
else:
    print("Constructing new model...")
    tai = intelligence.TetrisAI()  

# variables to track
training_started_at:float = time.time()
trained_experiences:int = 0 # the number of "experiences" (moves) the model has been trained on

# train!
gs:tetris.GameState = tetris.GameState()
while True:

    # collect a certain number of experiences
    experiences:list[intelligence.Experience] = []
    GameScores:list[int] = []
    rewards:list[float] = [] # list of rewards granted for each move. Can avg. this to get the avg reward in this episode.
    for i in range(0, collect_experiences):

        # prepare status
        status:str = "\r" + "Model trained on " + str(trained_experiences) + " experiences: "
        if len(rewards) > 0: status = status + "(" + str(round(sum(rewards) / len(rewards), 1)) + " avg reward over " + str(len(rewards)) + " moves) "
        if len(GameScores) > 0: status = status + "(" + str(round(sum(GameScores) / len(GameScores), 1)) + " avg score over " + str(len(GameScores)) + " games) "
        status = status + "Collecting experience # " + str(i+1) + " / " + str(collect_experiences) + "... "

        # print
        sys.stdout.write(status)
        sys.stdout.flush()

        # create new piece that will have to be decided on what move to play
        p:tetris.Piece = tetris.Piece()
        p.randomize()

        # prepare the piece and board as a representation (state) that could be passed to the model
        state_piece:list[int] = representation.PieceState(p)
        state_board:list[int] = representation.BoardState(gs)

        # select what move to play
        move:int
        if tools.oddsof(epsilon): # if, by chance (chance determined by epsilon as part of e-greedy), select a random move
            if p.width == 4: # one shape
                move = random.randint(0, 6)
            elif p.width == 3: # most scenarios
                move = random.randint(0, 7)
            elif p.width == 2: # one shape
                move = random.randint(0, 8) 
        else:
            move = tools.highest_index(tai.predict(state_piece, state_board)) # select the index of the highest value (highest perceived reward) out of the whole prediction of Q-Values.

        # record the score BEFORE
        score_before:float = gs.score_plus()

        # play the move
        IllegalMovePlayed:bool = False
        try:
            gs.drop(p, move)
        except tetris.InvalidShiftException as ex: # the model tried to play an illegal move
            IllegalMovePlayed = True
        except Exception as ex:
            print("Unhandled exception in move execution: " + str(ex))
            input("Press enter key to continue, if you want to.")

        # record score after
        score_after:float = gs.score_plus()
        if IllegalMovePlayed:
            score_after = score_before # No reward if an illegal move is played

        # calculate the reward from this action
        reward:float = score_after - score_before
        rewards.append(reward)

        # come up with a random piece that will be used as a dummy "next piece" in the next state.
        # since the piece generation is always random, it doesnt matter that the next piece is ACTUALLY the next piece.
        next_piece:tetris.Piece = tetris.Piece()
        next_piece.randomize()

        # store this scenario as an experience
        exp:intelligence.Experience = intelligence.Experience()
        exp.state = (state_piece, state_board)
        exp.action = move
        exp.reward = reward
        exp.next_state = (representation.PieceState(next_piece), representation.BoardState(gs)) # technically, if the game is over, this isn't even needed. It won't even be considered!
        exp.done = gs.over() or IllegalMovePlayed # if the game is over or IllegalMovePlayed... if either of those are true, mark as game over!
        experiences.append(exp)

        # if game is over, reset game!
        if gs.over() or IllegalMovePlayed:
            GameScores.append(gs.score())
            gs = tetris.GameState() # new game!
    print()

    # log performance to file
    avg_reward:float = round(sum(rewards) / len(rewards), 1)
    avg_score:float = round(sum(GameScores) / len(GameScores), 1)
    elapsed_seconds:float = time.time() - training_started_at # elapsed time since this training thing started, in seconds
    h,m,s = tools.convert_seconds(elapsed_seconds)
    tools.log(log_file_path, str(h) + " hours, " + str(m) + " minutes, " + str(s) + ", seconds: " + "model trained on " + str(trained_experiences) + " experiences = " + str(avg_reward) + " avg reward over " + str(len(rewards)) + " moves, " + str(avg_score) + " avg score over " + str(len(GameScores)) + " games.")

    # select a random subset of the experiences to train on
    ExperiencesToTrainOnCount:int = int(math.floor(len(experiences) * train_on_percent_of_experiences_batch))
    ExperiencesToTrainOn:list[intelligence.Experience] = random.sample(experiences, ExperiencesToTrainOnCount)

    # train on every experience
    print(str(len(experiences)) + " experiences collected! Time to train on " + str(len(ExperiencesToTrainOn)) + " of them (" + str(round(train_on_percent_of_experiences_batch*100,0)) + "% of them)")
    for exp in ExperiencesToTrainOn:

        new_target:float # "new_target" is essentially the 'correct' Q-Value that we want the Neural Network to learn for that particular state and action it did. In other words, we are going to set this to the updated current/future reward blend, plug this value into the prediction array, and then train on it.

        # determine what new_target is based upon the game ending or not
        if exp.done: # if game is over
            new_target = exp.reward
        else: # game is not done! There is still more game to go. So we should also consider FUTURE rewards as part or our (the NN's) understanding of what rewards this move will reap, now, or into the future.
            max_q_value_of_next_state = max(tai.predict(exp.next_state[0], exp.next_state[1])) # this is the "best Q value" of the NEXT state. Which will ALSO consider the Q-value of the NEXT STATE. And that goes on and on, like recursively. So really, every Q-value, to an extent (controlled by gamma), is also an estimation of future rewards.
            new_target = reward + (gamma * max_q_value_of_next_state) # gamma here serves as a slider scale, essentially setting "how important" the future rewards are vs. the current IMMEDIATE reward. i.e. if gamma was 0, it wouldn't consider the future at all, would just focus on the reward it got for THIS move only.

        # ask the model to predict again, for this experience's state (let me see the Q-value for each move again)
        qvalues:list[float] = tai.predict(exp.state[0], exp.state[1])

        # plug in the target where it belongs
        qvalues[exp.action] = new_target

        # Now, with this new UPDATED qvalues (well, with only 1 changed), train!
        tai.train(exp.state[0], exp.state[1], qvalues)
        trained_experiences = trained_experiences + 1
    experiences.clear() # dump the memory of experiences now that we trained on all those.

    