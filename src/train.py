import intelligence
import sys
import tools

### SETTINGS ###
model_save_path = r"" # if you want to start from a checkpoint, fill this in with the path to the .keras file. If wanting to start from a new NN, leave blank!
log_file_path:str = r"" # during training, if you want logs to be saved in this file about the progress of performance improvemnts during training, put a path to a txt file here. Logs will be appended.

# settings for training
games_in_batch:int = 100 # how many games will be played (simulated), with the top X% being used to train
best_game_focus:int = 10 # the top X games that will be trained on
accrue_games_before_training:int = 100 # the number of TOP games (games that will be trained on) which will be collected before it trains on them
training_epochs:int = 30 # the number of epochs those accrued good games are trained on
total_games:int = 100000 # the total number of games to train on. Once the model has been trained on this number, it will stop
save_checkpoint_every_trained:int = 1000 # after training each X number of games, a checkpoint will be saved
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

# numbers to track
games_trained:int = 0
on_checkpoint:int = 0
games_trained_at_last_checkpoint:int = 0

# train!
while games_trained < total_games:

    # collect games to train on by playing continuously, over and over
    scores:list[int] = [] # all of the scores that have been played so far by this model version (in this current state, before the next training)
    GamesToTrainOn:list[intelligence.PlayedGame] = [] # the top games that we will train on later
    while len(GamesToTrainOn) < accrue_games_before_training:

        status:str = "(" + str(games_trained) + " trained / " + str(total_games) + " goal) (" + str(len(GamesToTrainOn)) + " accrued / " + str(accrue_games_before_training) + " batch goal)"

        # play (simulate) a small-ish batch of games
        GameSimulations:list[intelligence.PlayedGame] = []
        for x in range(0, games_in_batch):
            status_line:str = "\r" + status + " " + "Simulating game # " + str(x+1) + " / " + str(games_in_batch)
            sys.stdout.write(status_line) # write the update
            sys.stdout.flush() # clear the current line
            pg = intelligence.simulate_game(tai)
            scores.append(pg.final_score) # append final score to the ongoing list
            GameSimulations.append(pg) # add this game to the list of games played
        print() # go to next line

        # calculate and print the average score of that batch of games
        batch_score_sum:int = 0
        for pg in GameSimulations:
            batch_score_sum = batch_score_sum + pg.final_score
        print("Avg. score of this episode, over " + str(len(scores)) + " games: " + str(round(sum(scores) / len(scores), 1)))

        # sort that batch of games by score, highest to lowest
        print("Sorting " + str(len(GameSimulations)) + " games by score...")
        GameSimulationsOrdered:list[intelligence.PlayedGame] = []
        while len(GameSimulations) > 0:
            best:intelligence.PlayedGame = GameSimulations[0]
            for pg in GameSimulations:
                if pg.final_score > best.final_score:
                    best = pg
            GameSimulationsOrdered.append(best)
            GameSimulations.remove(best)

        # take the top X games and put them in a list that we will train on later
        print("Selecting best " + str(best_game_focus) + " games for future training...")
        for i in range(best_game_focus): # take the top ones
            GamesToTrainOn.append(GameSimulationsOrdered[i])

        # get avg score of best group
        score:int = 0
        for pg in GamesToTrainOn:
            score = score + pg.final_score
        avg_score_best = score / len(GamesToTrainOn)
        print("Avg. score of " + str(best_game_focus) + " BEST games from that last batch of " + str(games_in_batch) + ": " + str(round(avg_score_best,1)))
    
    # if they provided a log file path, log the average performance in there
    if log_file_path != None and log_file_path != "":
        tools.log(log_file_path, "Avg score over " + str(len(scores)) + " games of model trained on " + str(games_trained) + " games: " + str(round(sum(scores) / len(scores), 1)))

    # we now have enough games accrued to start training, train now!
    print(str(len(GamesToTrainOn)) + " games reached. Entering training phase...")
    tai.train(GamesToTrainOn, training_epochs)
    games_trained = games_trained + len(GamesToTrainOn)
    print("Training complete! Total games trained now @ " + str(games_trained) + " out of goal of " + str(total_games) + ".")

    # is it time to save a checkpoint?
    if (games_trained - games_trained_at_last_checkpoint) >= save_checkpoint_every_trained: # it is time to save a checkpoint
        path:str = r"C:\Users\timh\Downloads\tah\tetris-ai\checkpoints\checkpoint" + str(on_checkpoint) + ".keras"
        tai.save(path)
        print("Checkpoint # " + str(on_checkpoint) + " saved to " + path + "!")
        on_checkpoint = on_checkpoint + 1
        games_trained_at_last_checkpoint = games_trained
