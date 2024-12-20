import intelligence
import sys

### SETTINGS ###
save_path = r"C:\Users\timh\Downloads\tah\tetris-ai\checkpoint.keras" # if you want to start from a checkpoint, fill this in with the path to the .keras file. If wanting to start from a new NN, leave blank!

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
if save_path != None and save_path != "":
    print("Loading model checkpoint at '" + save_path + "'...")
    tai = intelligence.TetrisAI(save_path)
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

    GamesToTrainOn:list[intelligence.PlayedGame] = [] # the top games that we will train on later
    avg_score:float = 0.0 # will be reported on during training so user watching can track progress
    while len(GamesToTrainOn) < accrue_games_before_training:

        status:str = "(" + str(games_trained) + " trained / " + str(total_games) + " goal) (" + str(len(GamesToTrainOn)) + " accrued / " + str(accrue_games_before_training) + " batch goal) (" + str(round(avg_score, 1)) + " avg score)"

        # play (simulate) games
        GameSimulations:list[intelligence.PlayedGame] = []
        for x in range(0, games_in_batch):
            status_line:str = "\r" + status + " " + "Simulating game # " + str(x+1) + " / " + str(games_in_batch)
            sys.stdout.write(status_line) # write the update
            sys.stdout.flush() # clear the current line
            pg = intelligence.simulate_game(tai)
            GameSimulations.append(pg)
        print() # go to next line

        # get avg score
        score:int = 0
        for pg in GameSimulations:
            score = score + pg.final_score
        avg_score = score / len(GameSimulations)
        print("Avg score of this group of " + str(len(GameSimulations)) + " simulations: " + str(avg_score))

        # sort by score
        print("Sorting " + str(len(GameSimulations)) + " games by score...")
        GameSimulationsOrdered:list[intelligence.PlayedGame] = []
        while len(GameSimulations) > 0:
            best:intelligence.PlayedGame = GameSimulations[0]
            for pg in GameSimulations:
                if pg.final_score > best.final_score:
                    best = pg
            GameSimulationsOrdered.append(best)
            GameSimulations.remove(best)

        # take the top X games and store them
        print("Selecting best " + str(best_game_focus) + " games for future training...")
        for i in range(best_game_focus): # take the top ones
            GamesToTrainOn.append(GameSimulationsOrdered[i])

        # get avg score of best group
        score:int = 0
        for pg in GamesToTrainOn:
            score = score + pg.final_score
        avg_score = score / len(GamesToTrainOn)
        print("Avg score of best " + str(best_game_focus) + " games: " + str(avg_score))
    
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
