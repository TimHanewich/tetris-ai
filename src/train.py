import intelligence
import sys
import tools
import tetris
import representation
import random

### SETTINGS ###
model_save_path = r"" # if you want to start from a checkpoint, fill this in with the path to the .keras file. If wanting to start from a new NN, leave blank!
log_file_path:str = r"C:\Users\timh\Downloads\tah\tetris-ai\checkpoints\log.txt" # during training, if you want logs to be saved in this file about the progress of performance improvemnts during training, put a path to a txt file here. Logs will be appended.

# training settings
gamma:float = 0.5
epsilon:float = 0.2
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

# train!
experiences:list[intelligence.Experience] = []
gs:tetris.GameState = tetris.GameState()
for epoch in range(0, 1000000000):
    print("On epoch " + str(epoch) + "... ")

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
        score_after = 0.0

    # calculate the reward from this action
    reward:float = score_after - score_before

    # come up with a random piece that will be used as a dummy "next piece" in the next state.
    # since the piece generation is always random, it doesnt matter that the next piece is ACTUALLY the next piece.
    next_piece:tetris.Piece = tetris.Piece()
    next_piece.randomize()

    # store this scenario as an experience
    exp:intelligence.Experience = intelligence.Experience()
    exp.state = (state_piece, state_board)
    exp.action = move
    exp.reward = reward
    exp.next_state = (representation.PieceState(next_piece), representation.BoardState(gs))
    exp.done = gs.over()
    experiences.append(exp)

    # train!
    if len(experiences) >= 32: # if we have accrued a certain batch size number
        print("Recorded experiences has reached " + str(len(experiences)) + " experiences. Time to train!")

        # train on every experience
        for exp in experiences:

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

        # dump the memory of experiences
        experiences.clear()

    # if game is over, reset game!
    if gs.over():
        print("Game is complete w/ final score of " + str(gs.score()) + "! Resetting.")
        gs = tetris.GameState() # new game!