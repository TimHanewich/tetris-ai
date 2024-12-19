## Neural Network Design
- **36 inputs**
    - 4 inputs that describes the new piece that must be dropped (`0` or `1` based on the square's occupancy). *Map described here: https://i.imgur.com/cFzaaeJ.png*
    - 32 inputs that describe the board (`0` or `1` based on the square's occupancy). *Map described here: https://i.imgur.com/cFzaaeJ.png*
- **4 outputs**, each one representing how many spaces to the right the shift input was (the only player-controlled input)
    - Output #1 = 0 Shift
    - Output #2 = 1 Shift
    - Output #3 = 2 Shift
    - Output #4 = 3 Shift (sometimes a 3 shift will be an invalid move. When this happens, the game will be deemed over and the score will be 0, significantly penalizing *against* this decision when it is illegal (a piece with width of 2))

## How training will work, example
- Model plays 300 games
- The best 30 games are selected and stored to an array
- The above loop continues until 500 games to train on are reached
- The 500 games are trained on against X number of epochs
- The above process repeats X times (until it has trained on ~10,000 games)

## Model Checkpoints, with Descriptions
|Checkpoint|Commit|Description|
|-|-|-|
|[download](https://github.com/TimHanewich/tetris-ai/releases/download/1/checkpoint14.keras)|`be880bb6decf65e8d3c7356aa235f011550d7a36`|First attempt at NN structure, all a flat layer. Self-played and trained on 14,000 games. Achieves an average score around 21-22 it seems|