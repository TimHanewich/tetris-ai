import random


class Piece:
    def __init__(self):
        self.squares:list[list[bool]] = [[False, False, False, False], [False, False, False, False]] # 2 rows of 4 columns

    def shape(self, id:str) -> None:
        """Adopts a shape of one of the seven standard tetris Tetriminos (https://tetris.fandom.com/wiki/Tetromino)"""
        
        official_shapes:list[str] = ["I","O","T","S","Z","J","L"]
        if id.upper() not in official_shapes:
            raise Exception("Unable to adopt shape '" + id + "' as that is not a known Tetrimino shape! Must be one from this list: " + str(official_shapes))
        
        # adopt the shape
        if id.upper() == "I":
            self.squares[0][0] = False
            self.squares[0][1] = False
            self.squares[0][2] = False
            self.squares[0][3] = False
            self.squares[1][0] = True 
            self.squares[1][1] = True
            self.squares[1][2] = True
            self.squares[1][3] = True
        elif id.upper() == "J":
            self.squares[0][0] = True
            self.squares[0][1] = False
            self.squares[0][2] = False
            self.squares[0][3] = False
            self.squares[1][0] = True 
            self.squares[1][1] = True
            self.squares[1][2] = True
            self.squares[1][3] = False
        elif id.upper() == "L":
            self.squares[0][0] = False
            self.squares[0][1] = False
            self.squares[0][2] = True
            self.squares[0][3] = False
            self.squares[1][0] = True 
            self.squares[1][1] = True
            self.squares[1][2] = True
            self.squares[1][3] = False
        elif id.upper() == "O":
            self.squares[0][0] = True
            self.squares[0][1] = True
            self.squares[0][2] = False
            self.squares[0][3] = False
            self.squares[1][0] = True 
            self.squares[1][1] = True
            self.squares[1][2] = False
            self.squares[1][3] = False
        elif id.upper() == "S":
            self.squares[0][0] = False
            self.squares[0][1] = True
            self.squares[0][2] = True
            self.squares[0][3] = False
            self.squares[1][0] = True 
            self.squares[1][1] = True
            self.squares[1][2] = False
            self.squares[1][3] = False
        elif id.upper() == "T":
            self.squares[0][0] = False
            self.squares[0][1] = True
            self.squares[0][2] = False
            self.squares[0][3] = False
            self.squares[1][0] = True 
            self.squares[1][1] = True
            self.squares[1][2] = True
            self.squares[1][3] = False
        elif id.upper() == "Z":
            self.squares[0][0] = True
            self.squares[0][1] = True
            self.squares[0][2] = False
            self.squares[0][3] = False
            self.squares[1][0] = False 
            self.squares[1][1] = True
            self.squares[1][2] = True
            self.squares[1][3] = False

    def randomize(self) -> None:
        """Adopts the shape of a random Tetrimino."""
        r:int = random.randint(0, 6) # pick a number between 0 and 6, including the 0 and 6
        if r == 0:
            self.shape("I")
        elif r == 1:
            self.shape("J")
        elif r == 2:
            self.shape("L")
        elif r == 3:
            self.shape("O")
        elif r == 4:
            self.shape("S")
        elif r == 5:
            self.shape("T")
        elif r == 6:
            self.shape("Z")

    def __str__(self):
        ToReturn = ""
        ToReturn = " ┌────┐" + "\n"
        onRow:int = 0
        for row in self.squares:
            ToReturn = ToReturn + str(onRow) +  "│"
            for column in row:
                if column:
                    ToReturn = ToReturn + "█"
                else:
                    ToReturn = ToReturn + " "
            ToReturn = ToReturn + "│\n"
            onRow = onRow + 1
        ToReturn = ToReturn + " └────┘"
        ToReturn = ToReturn + "\n" + "  0123"
        return ToReturn

    @property
    def width(self) -> int:
        ToReturn:int = 0
        if self.squares[0][0] or self.squares[1][0]: # if column A has something in it, add one
            ToReturn = ToReturn + 1
        if self.squares[0][1] or self.squares[1][1]: # if column B has something in it, add one
            ToReturn = ToReturn + 1
        if self.squares[0][2] or self.squares[1][2]: # if column C has something in it, add one
            ToReturn = ToReturn + 1
        if self.squares[0][3] or self.squares[1][3]: # if column D has something in it, add one
            ToReturn = ToReturn + 1
        return ToReturn

class InvalidShiftException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class GameState:
    def __init__(self):
        self.board:list[list[bool]] = [[False,False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False,False],[False,False,False,False,False,False,False,False,False,False]] # 20 rows of 10 columns

    def __str__(self):
        ToReturn:str = ""
        ToReturn = "  ┌──────────┐" + "\n"
        onRow:int = 0
        for row in self.board:

            # add the row number in
            if onRow >= 10:
                ToReturn = ToReturn + str(onRow) + "│"
            else: # if it is a single-digit, add in an extra space so it all lines up
                ToReturn = ToReturn + " " + str(onRow) + "│" 

            # print every square
            for column in row:
                if column:
                    ToReturn = ToReturn + "█"
                else:
                    ToReturn = ToReturn + " "
            ToReturn = ToReturn + "│\n"
            onRow = onRow + 1
        ToReturn = ToReturn + "  └──────────┘"
        ToReturn = ToReturn + "\n" + "   0123456789"
        return ToReturn
    
    def column_depths(self) -> list[int]:
        """Calculates how 'deep' the available space on each column (10 columns) goes, from the top down."""

        # record the depth of every column
        column_depths:list[int] = [0,0,0,0,0,0,0,0,0,0]
        column_collisions:list[bool] = [False, False, False, False, False, False, False, False, False, False] # records whether we have "reached the floor" of this column, a.k.a. reached a square that is occupied.

        # find the depth of each column 
        # In this sense, "depth" is the number of squares that are clear, to be clear
        for ri in range(0, len(self.board)): # for every row   
            for ci in range(0, len(self.board[0])): # for every column (use first row to know how many columns there are)
                if column_collisions[ci] == False and self.board[ri][ci] == False: # if column X has not been recorded yet and the column in this row is not occupied, increment the depth
                    column_depths[ci] = column_depths[ci] + 1
                else: # we hit a floor!
                    column_collisions[ci] = True

        return column_depths
    
    def drop(self, p:Piece, shift:int) -> None:
        """Drops a piece into the board, shifting it horizontally a number of columns."""
        
        # ensure shift is within bounds
        if shift < 0 or shift > 8: # the shift will NEVER be more than 8. Because the smallest piece is 2-wide, which would be a shift of 8
            raise Exception("Shift must be between 0 and 8")

        # ensure they are not trying to shift and do an illegal move
        if shift == 8 and p.width > 2:
            raise InvalidShiftException("Shift of " + str(shift) + " not possible for this piece as it is too wide!")
        if shift == 7 and p.width >= 4:
            raise InvalidShiftException("Shift of " + str(shift) + " not possible for this piece as it is too wide!")

        # calculate column depths
        column_depths:list[int] = self.column_depths()

        # get target column depths
        target_column_depths:list[int] = []
        for shifti in range(shift, shift + p.width):
            if shifti <= 9: # do not go beyond bounds of board (horizontally)
                target_column_depths.append(column_depths[shifti])

        # add potential "travel distance" based on the "floor" (bottom row square) of the piece having gaps
        for column_index in range(0, len(target_column_depths)):
            if p.squares[1][column_index] == False:
                target_column_depths[column_index] = target_column_depths[column_index] + 1

        # the drop depth is the minimum drop depth of every target column (after considering gaps, which we did)
        drop_depth:int = min(target_column_depths)

        # if drop depth is 0, that means there is just NO MORE ROOM!
        if drop_depth == 0:
            raise Exception("Unable to drop piece because there is no more room left to accomodate the piece!")
        
        # drop by "copying in the values"
        for row_index in range(0, len(p.squares)):
            for col_index in range(0, len(p.squares[row_index])):
                if p.squares[row_index][col_index]: # if the square of this piece is occupied
                    
                    # set "subtractor". This manual thing is needed so we aren't "flipping" (mirroring) the shape vertically when copying
                    subtractor:int
                    if row_index == 0:
                        subtractor = 2
                    elif row_index == 1:
                        subtractor = 1

                    self.board[drop_depth - subtractor][shift + col_index] = True
    
    def over(self) -> bool:
        """Checks if the game is over, determined by if there is at least a single square in the top row occupied"""
        for column in self.board[0]:
            if column:
                return True
        return False
    
    def score(self) -> int:
        """Returns a score of the game, the number of squares occupied."""
        ToReturn:int = 0
        for row in self.board:
            for column in row:
                if column:
                    ToReturn = ToReturn + 1
        return ToReturn
    
    def row_full(self, row) -> bool:
        """Returns True if every column (file) of a particular row is occupied."""
        return self.board[row][0] and self.board[row][1] and self.board[row][2] and self.board[row][3]
    
    def reward(self) -> float:
        """Returns a rough estimate for how successful the game was, considering more than just the score (i.e. also considering density of rows)"""

        ToReturn:float = float(self.score())

        # reward for each row being full, but more for certain rows
        if self.row_full(0): ToReturn = ToReturn + 0.5
        if self.row_full(1): ToReturn = ToReturn + 0.8
        if self.row_full(2): ToReturn = ToReturn + 1.0
        if self.row_full(3): ToReturn = ToReturn + 1.2
        if self.row_full(4): ToReturn = ToReturn + 1.4
        if self.row_full(5): ToReturn = ToReturn + 1.6
        if self.row_full(6): ToReturn = ToReturn + 1.8
        if self.row_full(7): ToReturn = ToReturn + 2.0

        return ToReturn