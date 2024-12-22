import random


class Piece:
    def __init__(self):
        self.squares:list[list[bool]] = [[False, False], [False, False]] # 2 rows of 2 columns

    def __str__(self):
        ToReturn = ""
        ToReturn = " ┌──┐" + "\n"
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
        ToReturn = ToReturn + " └──┘"
        ToReturn = ToReturn + "\n" + "  01"
        return ToReturn

    def randomize(self) -> None:
        r:int = random.randint(0, 6) # pick a number between 0 and 6, including the 0 and 6

        if r == 0:
            self.squares[0][0] = False
            self.squares[1][0] = True
            self.squares[0][1] = False
            self.squares[1][1] = False
        elif r == 1:
            self.squares[0][0] = False
            self.squares[1][0] = True
            self.squares[0][1] = False
            self.squares[1][1] = True
        elif r == 2:
            self.squares[0][0] = True
            self.squares[1][0] = True
            self.squares[0][1] = False
            self.squares[1][1] = False
        elif r == 3:
            self.squares[0][0] = True
            self.squares[1][0] = True
            self.squares[0][1] = True
            self.squares[1][1] = False
        elif r == 4:
            self.squares[0][0] = True
            self.squares[1][0] = False
            self.squares[0][1] = True
            self.squares[1][1] = True
        elif r == 5:
            self.squares[0][0] = True
            self.squares[1][0] = True
            self.squares[0][1] = False
            self.squares[1][1] = True
        elif r == 6:
            self.squares[0][0] = False
            self.squares[1][0] = True
            self.squares[0][1] = True
            self.squares[1][1] = True
    
    def columns_occupied(self) -> int:
        """Checks how many columns the piece is occupying (1 or 2)"""
        if self.squares[0][1] or self.squares[1][1]:
            return 2
        elif self.squares[0][0] or self.squares[1][0]:
            return 1
        else:
            return 0

    @property
    def width(self) -> int:
        ToReturn:int = 0
        if self.squares[0][0] or self.squares[1][0]: # if column A has something in it, add one
            ToReturn = ToReturn + 1
        if self.squares[0][1] or self.squares[1][1]: # if column B has something in it, add one
            ToReturn = ToReturn + 1
        return ToReturn

class InvalidShiftException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class GameState:
    def __init__(self):
        self.board:list[list[bool]] = [[False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False]] # 8 rows of 4 columns

    def __str__(self):
        ToReturn:str = ""
        ToReturn = " ┌────┐" + "\n"
        onRow:int = 0
        for row in self.board:
            ToReturn = ToReturn + str(onRow) + "│"
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
    
    def column_depths(self) -> list[int]:
        """Calculates how 'deep' the available space on each column (4 columns) goes."""

        # record the depth of every column
        column_depths:list[int] = [0,0,0,0]
        column_collisions:list[bool] = [False, False, False, False] # records whether we have "reached the floor" of this column, a.k.a. reached a square that is occupied.

        # find the depth of each column 
        # In this sense, "depth" is the number of squares that are clear, to be clear
        for ri in range(0, len(self.board)):    
            for ci in range(0, 4):
                if column_collisions[ci] == False and self.board[ri][ci] == False: # if column X has not been recorded yet and the column in this row is not occupied, increment the depth
                    column_depths[ci] = column_depths[ci] + 1
                else: # we hit a floor!
                    column_collisions[ci] = True

        return column_depths
    
    def drop(self, p:Piece, shift:int) -> None:
        """Drops a piece into the board, shifting it horizontally a number of columns."""
        
        # ensure shift is within bounds
        if shift < 0 or shift > 3:
            raise Exception("Shift must be between 0 and 3")

        # firstly, if they are trying to shift THREE spaces, ensure none of the second column is occupied. That is the only way that a shift of three is even possible (can't "extend" column B beyond the limits of the board)
        if shift == 3 and (p.squares[0][1] or p.squares[1][1]):
            raise InvalidShiftException("Cannot shift piece 3 units to the right because the piece has column B occupied.")

        # calculate column depths
        column_depths:list[int] = self.column_depths()

        # determine the drop depth, the minimum depth of the target columns
        drop_depth:int = 0
        if shift == 3:
            drop_depth = column_depths[shift]
        else:

            # get existing depth of columns
            columnA_depth:int = column_depths[shift]
            columnB_depth:int = column_depths[shift + 1]
            
            # add "travel distance" based on the shape of the piece
            if p.squares[1][0] == False: # if bottom left is not occupied, add one
                columnA_depth = columnA_depth + 1
                if p.squares[0][0] == False: # if top left is also not occupied, add infinity! There is nothing here that would stop any vertical movement!
                    columnA_depth = columnA_depth + 999
            if p.squares[1][1] == False: # if bottom right is not occupied, add one
                columnB_depth = columnB_depth + 1
                if p.squares[0][1] == False: # if top right is not occupied, add infinity! There is nothing here that would stop any vertical movement!
                    columnB_depth = columnB_depth + 999

            drop_depth:int = min(columnA_depth, columnB_depth)

        # if drop depth is 0, that means there is just NO MORE ROOM!
        if drop_depth == 0:
            raise Exception("Unable to drop piece because there is no more room left to accomodate the piece!")

        # drop by "copying in" the values
        # note that we are only "copying" over the TRUE values. We do not want to CLEAR a square on the board if the square of the piece is not occupied... that may cause an accidental clearing of a square on the board.
        if p.squares[1][0]: self.board[drop_depth - 1][shift] = p.squares[1][0] # bottom left
        if p.squares[0][0]: self.board[drop_depth - 2][shift] = p.squares[0][0] # top left
        if p.squares[1][1]: self.board[drop_depth - 1][shift + 1] = p.squares[1][1] # bottom right
        if p.squares[0][1]: self.board[drop_depth - 2][shift + 1] = p.squares[0][1] # top right
    
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