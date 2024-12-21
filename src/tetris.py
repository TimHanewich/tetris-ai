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
                    ToReturn = ToReturn + "X"
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
                    ToReturn = ToReturn + "X"
                else:
                    ToReturn = ToReturn + " "
            ToReturn = ToReturn + "│\n"
            onRow = onRow + 1
        ToReturn = ToReturn + " └────┘"
        ToReturn = ToReturn + "\n" + "  0123"
        return ToReturn
    
    def drop(self, p:Piece, shift:int) -> None:
        """Drops a piece into the board, shifting it horizontally a number of columns."""
        
        # ensure shift is within bounds
        if shift < 0 or shift > 3:
            raise Exception("Shift must be between 0 and 3")

        # firstly, if they are trying to shift THREE spaces, ensure none of the second column is occupied. That is the only way that a shift of three is even possible (can't "extend" column B beyond the limits of the board)
        if shift == 3 and (p.squares[0][1] or p.squares[1][1]):
            raise InvalidShiftException("Cannot shift piece 3 units to the right because the piece has column B occupied.")

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
                if p.squares[0][0] == False: # if top left is also not occupied, add one
                    columnA_depth = columnA_depth + 1
            if p.squares[1][1] == False: # if bottom right is not occupied, add one
                columnB_depth = columnB_depth + 1
                if p.squares[0][1] == False: # if top right is not occupied, add one
                    columnB_depth = columnB_depth + 1

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