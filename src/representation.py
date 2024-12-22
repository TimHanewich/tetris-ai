import tetris

def PieceState(p:tetris.Piece) -> list[int]:
    ToReturn:list[int] = []
    ToReturn.append(int(p.squares[0][0]))
    ToReturn.append(int(p.squares[1][0]))
    ToReturn.append(int(p.squares[0][1]))
    ToReturn.append(int(p.squares[1][1]))
    ToReturn.append(int(p.squares[0][2]))
    ToReturn.append(int(p.squares[1][2]))
    ToReturn.append(int(p.squares[0][3]))
    ToReturn.append(int(p.squares[1][3]))
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