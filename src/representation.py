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
    """Returns the state of the board, expressed as a flattened array of integers, each being 0 or 1."""
    ToReturn:list[int] = []
    for r in range(0, len(gs.board)):
        for c in range(0, len(gs.board[0])):
            ToReturn.append(int(gs.board[r][c]))
    return ToReturn