# Epsilon, a.k.a. "e-greedy"
It can become very easy for the model to find a "local optimum" and just stick to it. For example, early on in training in this project, the early models would only choose one of two moves. It had found a local optimum and was stuck in this optimum.

To fix this, we have to encourage exploration. Encourage the model to do things that it *thinks* may not lead to success, but sacrifice this in favor of the possibility of finding a new strategy. So, we introduce randomness to our model.

## Explanation of e-greedy by Copilot
The ε-greedy strategy is a popular approach in reinforcement learning for balancing the trade-off between exploration and exploitation. Let's break it down:

Purpose of ε-Greedy
Exploration: This is about trying out new actions that the agent hasn't taken before. The purpose is to gather more information about the environment, which can help the agent discover better strategies and avoid getting stuck in a suboptimal solution.

Exploitation: This is about using the agent's current knowledge to take actions that it believes will yield the highest reward. The purpose is to maximize the immediate payoff based on what the agent has already learned.

How ε-Greedy Works
The ε-greedy strategy uses a parameter ε (epsilon) to decide whether the agent should explore or exploit in each step:

With probability ε: The agent chooses a random action, which promotes exploration.

With probability 1-ε: The agent chooses the best-known action, which promotes exploitation.

Trade-off Between Exploration and Exploitation
Balancing exploration and exploitation is crucial for effective learning:

Exploration Benefits:

Helps the agent learn about the environment.

Prevents the agent from settling too early on suboptimal strategies.

Allows the agent to discover new and potentially better actions.

Exploration Costs:

Might result in taking actions that yield low rewards in the short term.

Can slow down the immediate performance of the agent.

Exploitation Benefits:

Leverages the agent’s current knowledge to maximize rewards.

Enhances the performance based on the agent's learning.

Exploitation Costs:

Risk of missing out on better actions that have not been explored yet.

Can lead to suboptimal long-term performance if the agent gets stuck in a local optimum.

Dynamic Adjustment of ε
To balance this trade-off over time, ε is often adjusted dynamically:

Start with a high ε (e.g., 1.0) to encourage more exploration initially.

Gradually decrease ε over time (e.g., to 0.1 or even lower) as the agent learns more about the environment. This shift allows the agent to exploit its knowledge more as it becomes more confident in its learning.

## Explanation of what value to set e-greedy (epsilon) to by Copilot
Setting ε (epsilon) at 10% means your agent will explore 10% of the time and exploit the best-known actions 90% of the time. Whether this is a good value depends on the specific nature of your game and how well your agent has learned so far.

Here are some general guidelines:

Initial Phase of Learning: Higher values (e.g., 100% down to 30%) to encourage exploration. The agent needs to try out various actions to gather information about the environment.

Intermediate Phase: Moderate values (e.g., 30% down to 10%) to balance exploration and exploitation. The agent is still learning but should start leveraging its knowledge.

Later Phase: Lower values (e.g., 10% or lower) to focus more on exploitation, as the agent has gathered sufficient knowledge to make informed decisions.

You could start with a higher value (like 100% or 50%) and gradually decrease it as your agent learns more about the game environment. This decay can be linear, exponential, or adaptive based on performance.

Here's an example of decaying ε over time:

python
```
initial_epsilon = 1.0  # Start with full exploration
min_epsilon = 0.1      # Minimum exploration rate
decay_rate = 0.001     # Rate of decay for exploration

epsilon = initial_epsilon
for episode in range(total_episodes):
    # Choose action: random with probability epsilon, best known action otherwise
    if random.uniform(0, 1) < epsilon:
        action = random_action()
    else:
        action = best_known_action()

    # Perform action, observe reward and new state
    # Update Q-values or other learning mechanisms here
    
    # Decay epsilon
    epsilon = max(min_epsilon, epsilon - decay_rate)
```
Starting with ε at 10% might be fine if your agent already has a good understanding of the environment. However, if it's still in the early stages of learning, you might want to start with a higher ε and gradually reduce it.

How's the agent performing so far with the current settings? Any specific challenges or patterns you've noticed?