# Q-Learning 

## Summarized (in my own words)
Q Learning Process (*for all of this, think of the neural network as an estimation of a Q-table, a table of each possible state in the game and then the expected rewards for each action. That is what the NN is intended to be estimating*):

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
- Determine the correct "Q-Value" for each give experience memory, called "target"... 
    - if game is over, target is just the immediate reward. 
    - If game is not over we use the NN to predict the best Q-value for the NEXT STATE. And then blend this NEXT STATE Q-value with the immediate reward (using a discount factor). 
- We (again) ask the NN to predict for this experince's "before state" and get the array of Q-values.
- We plug in the target (new, correct "Q-Value") into the prediction array where it belongs, only changing that one thing.
- We train the model on one epoch on this this new array

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

## That Q-Learning portion with context from Copilot
```
for epoch in range(1000):
    state = env.reset()
    state = np.reshape(state, [1, 20, 10, 1])
    done = False
    previous_occupied_squares = np.sum(state)
    while not done:
        if np.random.rand() <= epsilon:
            action = random.randrange(env.action_space.n)
        else:
            q_values = model.predict(state)
            action = np.argmax(q_values)

        next_state, _, done, _ = env.step(action)
        next_state = np.reshape(next_state, [1, 20, 10, 1])

        current_occupied_squares = np.sum(next_state)
        reward = current_occupied_squares - previous_occupied_squares
        previous_occupied_squares = current_occupied_squares

        memory.append((state, action, reward, next_state, done))
        state = next_state

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
                
            if epsilon > epsilon_min:
                epsilon *= epsilon_decay

print("Training complete!")
```