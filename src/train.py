import intelligence
import tetris
import representation
import random
import sys
import tools

### SETTINGS ###
model_save_path = r"" # if you want to start from a checkpoint, fill this in with the path to the .keras file. If wanting to start from a new NN, leave blank!
log_file_path:str = r"C:\Users\timh\Downloads\tah\tetris-ai\checkpoints\log.txt" # during training, if you want logs to be saved in this file about the progress of performance improvemnts during training, put a path to a txt file here. Logs will be appended.

# training settings
gamma:float = 0.5
epsilon:float = 0.2

# training config
batch_size:int = 50 # the number of experiences that will be collected before training starts
save_model_every_experiences:int = 5000 # how many experiences must be trained before a new model checkpoint is saved
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
experiences_trained:int = 0 # the number of experiences the model has been trained at at any given point
model_last_saved_at_experiences_trained:int = 0 # the last number of experiences the model was trained on when the last checkpoint was saved
on_checkpoint:int = 0

# training loop!
while True:

    # collect X number of experiences
    gs = tetris.GameState()
    experiences:list[intelligence.Experience] = [] # collection off all the experiences
    GameScores:list[int] = [] # all of the scores of the finished games
    for ei in range(0, batch_size):

        # print
        sys.stdout.write("\r" + "Collecting experience " + str(ei+1) + " / " + str(batch_size) + "... ")
        sys.stdout.flush()

        # generate piece
        p = tetris.Piece()
        p.shape("O")

        # get piece & board representation
        repr_piece:list[int] = representation.PieceState(p)
        repr_board:list[int] = representation.BoardState(gs)

        # select what move to play
        move:int
        if random.random() < epsilon:
            if p.width == 2: # one shape
                move = random.randint(0, 8)
            elif p.width == 3: # most shapes
                move = random.randint(0, 7)
            elif p.width == 4: # one shape
                move = random.randint(0, 6)
        else:
            predictions:list[float] = tai.predict(repr_piece, repr_board)
            move = predictions.index(max(predictions)) # select the index with the highest Q-Value (highest expected reward)

        # Execute the move
        IllegalMovePlayed:bool = False
        MoveReward:float = 0.0
        try:
            MoveReward = gs.drop(p, move)
        except tetris.InvalidShiftException as ex:
            IllegalMovePlayed = True
            MoveReward = -5.0 # penalize for illegal moves
        except Exception as ex:
            print("Unhandled exeption in move execution: " + str(ex))
            input("Press enter key to continue, if you want to.")

        # create a random next piece for the sake of the "next state"
        np:tetris.Piece = tetris.Piece()
        np.shape("O")

        # store this experience
        exp:intelligence.Experience = intelligence.Experience()
        exp.state = (repr_piece, repr_board) # the situation that was presented to the neural network
        exp.action = move # the decision the neural network made (or was made by random chance via epsilon)
        exp.reward = MoveReward # the reward that was given from that move
        exp.next_state = (representation.PieceState(np), representation.BoardState(gs)) # the next state
        exp.done = gs.over() or IllegalMovePlayed # if the game is completed or terminated via it finishing or an illegal move being played
        experiences.append(exp)

        # if the game is over or an illegal move was played, reset
        if gs.over() or IllegalMovePlayed:
            GameScores.append(gs.score())
            gs = tetris.GameState() # new game!
    print("experience collection complete!")

    # calculate average rewards over that group of experiences
    rewards:float = 0.0
    for exp in experiences:
        rewards = rewards + exp.reward
    avg_reward = rewards / len(experiences)

    # print the progress!
    status:str = "Last " + str(len(experiences)) + " experiences by model trained on " + str(experiences_trained) + " experiences: " + str(round(avg_reward, 1)) + " avg. reward, " + str(round(sum(GameScores) / len(GameScores), 1)) + " avg. score over " + str(len(GameScores)) + " games played."
    tools.log(log_file_path, status)
    print(status)

    # train!
    for ei in range(0, len(experiences)):
        exp = experiences[ei]

        # print
        sys.stdout.write("\r" + "Training on experience " + str(ei+1) + " / " + str(len(experiences)) + "... ")
        sys.stdout.flush()

        # determine new target based on the game ending or not
        new_target:float
        if exp.done:
            new_target = exp.reward
        else:
            max_q_of_next_state:float = max(tai.predict(exp.next_state[0], exp.next_state[1]))
            new_target = exp.reward + (gamma * max_q_of_next_state) # blend immediate vs. future rewards

        # ask the model to predict again for this experiences state
        qvalues:list[float] = tai.predict(exp.state[0], exp.state[1])

        # plug in the new target where it belongs
        qvalues[exp.action] = new_target

        # now train on the updated qvalues (with 1 value changed)
        tai.train(exp.state[0], exp.state[1], qvalues)
        experiences_trained = experiences_trained + 1
    print("training complete!")

    # save model checkpoint
    if (experiences_trained - model_last_saved_at_experiences_trained) >= save_model_every_experiences:
        print("Time to save model!")
        path:str = r"C:\Users\timh\Downloads\tah\tetris-ai\checkpoints\checkpoint" + str(on_checkpoint) + ".keras"
        tai.save(path)
        print("Checkpoint # " + str(on_checkpoint) + " saved to " + path + "!")
        on_checkpoint = on_checkpoint + 1
        model_last_saved_at_experiences_trained = experiences_trained