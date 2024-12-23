# Q-Learning 

## Summarized (in my own words)
Q Learning Process:

We take the current state and calculate the current "score" of the game. 

The model predicts what move to play by a forward pass, estimating the "Q-value" (blend of current + future reward) for each move, and then selecting the move that gives it the highest Q-Value.

We play that move 

We record the current "score" of the game. 

The **reward** is the difference between the current score and the score that was before the move. 

We store memory of this experience into a temporary list with the following:
- before state
- action taken
- immediate reward from that action
- next state
- is game complete? (True/False)

After we have enough memories built up (like 300?), we will then train the NN to better predict Q-value (a blend of immediate + future rewards). So, we:
- Determine the correct "Q-Value" for each give experience memory, called "target"... if game is over, target is just the immediate reward. If game is not over we use the NN to predict the best Q-value for the NEXT STATE. And then blend this NEXT STATE Q-value with the immediate reward (using a discount factor). 
- We (again) ask the NN to predict for this experince's "before state"
- We plug in the target (new, correct "Q-Value") into the prediction array where it belongs, only changing that one thing.
- We train the model on one epoch on this this new pair. 

And this repeats over and over!

## Example Q-Learning Training portion from Copilot
```
if len(memory) > batch_size:
    minibatch = random.sample(memory, batch_size)
    for state, action, reward, next_state, done in minibatch:
        target = reward
        if not done:
            max_future_q_value = np.max(model.predict(next_state))
            target = reward + gamma * max_future_q_value
        
        target_f = model.predict(state)
        target_f[0][action] = target
        
        model.fit(state, target_f, epochs=1, verbose=0)
```

