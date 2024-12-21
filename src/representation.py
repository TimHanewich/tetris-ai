import tetris

def PieceState(p:tetris.Piece) -> list[int]:
    """Returns the number of spaces that are 'empty' from the bottom from the bottom up. In other words, for each column, looking from the bottom up, if the bottom-most square of that columns is occupied, that column would be 0. If it is not, it would be 1, but then if the top square is not, it would be 2. If the bottom square is occupied but the top is not occupied, it is still 0. Because at that point the top doesn't matter as long as the bottom square is occupied. If both in that column are not occoupeid, it would be 2 of course. So, it is like the 'empty squares from the bottom up' to explain it in different words."""

    ToReturn:list[int] = []

    # column A
    if p[1][0]:
        ToReturn.append(0)
    elif p[0][0]:
        ToReturn.append(1)
    else: # if both in the first column are not on, do 2.
        ToReturn.append(2)

    # column B
    if p[1][1]:
        ToReturn.append(0)
    elif p[0][1]:
        ToReturn.append(1)
    else: # if both in the first column are not on, do 2.
        ToReturn.append(2)

    return ToReturn
    

def BoardState(gs:tetris.GameState) -> list[int]:
    """Returns the relative available depth of the board."""

    columns_depth:list[int] = gs.column_depths()

    # subtract 1 from each until one is 0
    # doing this allows for the depth to be "relative"
    while 0 not in columns_depth:
        for i in range(0, len(columns_depth)):
            columns_depth[i] = columns_depth[i] - 1
    
    return columns_depth