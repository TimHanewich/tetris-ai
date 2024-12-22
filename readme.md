## Neural Network Design
- 6 input
    - **2 inputs for piece** (2 ints)
    - **4 inputs for board** (4 ints)
- **4 outputs**, each one representing how many spaces to the right the shift input was (the only player-controlled input)
    - Output #1 = 0 Shift
    - Output #2 = 1 Shift
    - Output #3 = 2 Shift
    - Output #4 = 3 Shift (sometimes a 3 shift will be an invalid move. When this happens, the game will be deemed over and the score will be 0, significantly penalizing *against* this decision when it is illegal (a piece with width of 2))

## Model Checkpoints, with Descriptions
|Checkpoint|Commit|Description|
|-|-|-|
|[download](https://github.com/TimHanewich/tetris-ai/releases/download/1/checkpoint14.keras)|`be880bb6decf65e8d3c7356aa235f011550d7a36`|First attempt at NN structure, all a flat layer. Self-played and trained on 14,000 games. Achieves an average score around 21-22 it seems.|
|[download]()|`76d5f57a4bf488c0ada0ad5c1efac46d7084686a`|Second neural network structure (separate paths for piece + board). Trained on 11,000 games. Achieves an average score of around 21-22 it seems. I am quite certain the model fell into a "local optimum" and only plays moves `0` and moves `2`.|
|[download](https://github.com/TimHanewich/tetris-ai/releases/download/3/checkpoint8.keras)|`645024b176356ecab0ea210fce60e9fdd967ec14`|The last NN found a local optimum, so added a bit of randomizing to this one for purposes of exploration. But noticed there was a bug in the tetris `drop()` code.|
|[download](https://github.com/TimHanewich/tetris-ai/releases/download/4/checkpoint7.keras)|`f85bad9d693012988b57c0c4a3211a9efba14351`|Trained after fixing bug in drop logic (or I believe it is fixed now). Trained on 8,000 games. Log file can be found [here](https://github.com/TimHanewich/tetris-ai/releases/download/4/log.txt).|
|[download](https://github.com/TimHanewich/tetris-ai/releases/download/5/checkpoint0.keras)|`ea80581b8080e89c09b1b8716ee773046b9891ea`|Trained on 1,020 games. Used a quicker format for training, reached peak performance (~22) rather quickly compared to previous trainings. Log file [here](https://github.com/TimHanewich/tetris-ai/releases/download/5/log.txt).|
|[download](https://github.com/TimHanewich/tetris-ai/releases/download/6/checkpoint12.keras)|`05ce34283b35126e1e8a965b21ccac82b9c1cb72`|Moved to new "depth-based" board state representation. Trained on ~6,500 games. Performs ~22. Log [here](https://github.com/TimHanewich/tetris-ai/releases/download/6/log.txt).|
|[download](https://github.com/TimHanewich/tetris-ai/releases/download/7/checkpoint0.keras)|`cf9125cdc394ea836f091890f1f36a4c0891f797`|Introduced reward function that also considers rows being full. Trained on ~500 games. Quickly reached peak performance of ~25 but then fell to ~22. Log file [here](https://github.com/TimHanewich/tetris-ai/releases/download/7/log.txt).|
|[download]()|`b8c434386e4751dab6bc57e7566359e1c9628e1e`|Trained in 4 separate sessions of varying degrees of `epsilon`, resulting in a final consistent score (reported at least) or 28-29. See [this picture](https://i.imgur.com/99bq35K.png) for a description on each stage. Log file for all training sessions [here](https://github.com/TimHanewich/tetris-ai/releases/download/8/log.txt).|