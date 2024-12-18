## Neural Network Design
- **36 inputs**
    - 4 inputs that describes the new piece that must be dropped (`0` or `1` based on the square's occupancy). *Map described here: https://i.imgur.com/cFzaaeJ.png*
    - 32 inputs that describe the board (`0` or `1` based on the square's occupancy). *Map described here: https://i.imgur.com/cFzaaeJ.png*
- **4 outputs**, each one representing how many spaces to the right the shift input was (the only player-controlled input)
    - Output #1 = 0 Shift
    - Output #2 = 1 Shift
    - Output #3 = 2 Shift
    - Output #4 = 3 Shift (sometimes a 3 shift will be an invalid move. When this happens, the game will be deemed over and the score will be 0, significantly penalizing *against* this decision when it is illegal (a piece with width of 2))