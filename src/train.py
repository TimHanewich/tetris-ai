import intelligence
import sys
import tools

### SETTINGS ###
model_save_path = r"" # if you want to start from a checkpoint, fill this in with the path to the .keras file. If wanting to start from a new NN, leave blank!
log_file_path:str = r"C:\Users\timh\Downloads\tah\tetris-ai\checkpoints\log.txt" # during training, if you want logs to be saved in this file about the progress of performance improvemnts during training, put a path to a txt file here. Logs will be appended.

# settings for training
games_in_episode:int = 10 # how many games will be played (simulated), with the top X% being used to train
train_on_best_count:int = 3 # the number of TOP games (games that will be trained on) which will be trained on out of the episode
training_epochs:int = 10 # the number of epochs those accrued good games are trained on
save_checkpoint_every_trained:int = 150 # after training each X number of games, a checkpoint will be saved

# epsilon (exploration) settings
epsilon_initial:float = 0.50 # the initial epsilon value to start at
epsilon_decay:float = 0.01 # how much to decrease epsilon after each training
epsilon_min:float = 0.05 # the minimum exploration rate
################

# construct/load model`
tai:intelligence.TetrisAI = None
if model_save_path != None and model_save_path != "":
    print("Loading model checkpoint at '" + model_save_path + "'...")
    tai = intelligence.TetrisAI(model_save_path)
    print("Model loaded!")
else:
    print("Constructing new model...")
    tai = intelligence.TetrisAI()  

# numbers to track
games_trained:int = 0
on_checkpoint:int = 0
games_trained_at_last_checkpoint:int = 0

# train!
epsilon:float = epsilon_initial
while True:

    # collect games to train on by playing continuously, over and over
    scores:list[int] = [] # all of the scores that have been played so far in this episode
    GamesToTrainOn:list[intelligence.PlayedGame] = [] # the top games that we will train on later

    # play (simulate) all of the games we are supposed to per episode
    GameSimulations:list[intelligence.PlayedGame] = []
    for x in range(0, games_in_episode):

        # construct the line to write
        status_line:str = "\r" + "(" + str(games_trained) + " games trained)" + " (epsilon = " + str(round(epsilon,3)) + ") " + "Simulating game # " + str(x+1) + " / " + str(games_in_episode)
        
        # append avg score if there is at least one game yet (can't divide by 0!)
        if len(scores) > 0:
            avg_score_in_this_episode:float = round(sum(scores) / len(scores), 1)
            status_line = status_line + ", avg score = " + str(avg_score_in_this_episode)
        
        # print
        sys.stdout.write(status_line) # write the update
        sys.stdout.flush() # clear the current line

        # simulate and append
        pg = intelligence.simulate_game(tai, epsilon)
        scores.append(pg.final_score) # append final score to the ongoing list
        GameSimulations.append(pg) # add this game to the list of games played
    print() # go to next line

    # sort that all of this episode's games by score, highest to lowest
    print("Sorting " + str(len(GameSimulations)) + " games by reward...")
    GameSimulationsOrdered:list[intelligence.PlayedGame] = []
    while len(GameSimulations) > 0:
        best:intelligence.PlayedGame = GameSimulations[0]
        for pg in GameSimulations:
            if pg.final_reward > best.final_reward:
                best = pg
        GameSimulationsOrdered.append(best)
        GameSimulations.remove(best)

    # take the top X games and put them in a list that we will train on
    print("Selecting best " + str(train_on_best_count) + " games from this episode for training...")
    for i in range(train_on_best_count): # take the top ones
        GamesToTrainOn.append(GameSimulationsOrdered[i])

    # get avg score of best group
    score:int = 0
    for pg in GamesToTrainOn:
        score = score + pg.final_score
    avg_score_best = score / len(GamesToTrainOn)
    print("Avg. score of " + str(train_on_best_count) + " BEST games from that last batch of " + str(games_in_episode) + ": " + str(round(avg_score_best,1)))
    
    # if they provided a log file path, log the average performance in there
    tools.log(log_file_path, "Avg. score over " + str(len(scores)) + " games played by model trained on " + str(games_trained) + " games: " + str(round(sum(scores) / len(scores), 1)) + ". Avg. score of best " + str(len(GamesToTrainOn)) + " games from that episode we will now train on in preparation of next episode: " + str(round(avg_score_best, 1)))

    # Train!
    print("Entering training phase for these best " + str(len(GamesToTrainOn)) + " games")
    tai.train(GamesToTrainOn, training_epochs)
    games_trained = games_trained + len(GamesToTrainOn)
    print("Training complete! Total games trained now @ " + str(games_trained) + ".")

    # is it time to save a checkpoint?
    if (games_trained - games_trained_at_last_checkpoint) >= save_checkpoint_every_trained: # it is time to save a checkpoint
        path:str = r"C:\Users\timh\Downloads\tah\tetris-ai\checkpoints\checkpoint" + str(on_checkpoint) + ".keras"
        tai.save(path)
        print("Checkpoint # " + str(on_checkpoint) + " saved to " + path + "!")
        on_checkpoint = on_checkpoint + 1
        games_trained_at_last_checkpoint = games_trained

    # decrement (decay) epsilon, but don't go below minumum
    epsilon = max(epsilon - epsilon_decay, epsilon_min)