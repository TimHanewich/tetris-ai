import tetris

def PieceState(p:tetris.Piece) -> list[int]:
    ToReturn:list[int] = []

    # add piece
    ToReturn.append(int(p.squares[0][0]))
    ToReturn.append(int(p.squares[0][1]))
    ToReturn.append(int(p.squares[1][0]))
    ToReturn.append(int(p.squares[1][1]))

    return ToReturn

def BoardState(gs:tetris.GameState) -> list[int]:

    ToReturn:list[int] = []

    # add board by row
    ToReturn.append(int(gs.board[0][0]))
    ToReturn.append(int(gs.board[0][1]))
    ToReturn.append(int(gs.board[0][2]))
    ToReturn.append(int(gs.board[0][3]))

    ToReturn.append(int(gs.board[1][0]))
    ToReturn.append(int(gs.board[1][1]))
    ToReturn.append(int(gs.board[1][2]))
    ToReturn.append(int(gs.board[1][3]))

    ToReturn.append(int(gs.board[2][0]))
    ToReturn.append(int(gs.board[2][1]))
    ToReturn.append(int(gs.board[2][2]))
    ToReturn.append(int(gs.board[2][3]))

    ToReturn.append(int(gs.board[3][0]))
    ToReturn.append(int(gs.board[3][1]))
    ToReturn.append(int(gs.board[3][2]))
    ToReturn.append(int(gs.board[3][3]))

    ToReturn.append(int(gs.board[4][0]))
    ToReturn.append(int(gs.board[4][1]))
    ToReturn.append(int(gs.board[4][2]))
    ToReturn.append(int(gs.board[4][3]))

    ToReturn.append(int(gs.board[5][0]))
    ToReturn.append(int(gs.board[5][1]))
    ToReturn.append(int(gs.board[5][2]))
    ToReturn.append(int(gs.board[5][3]))

    ToReturn.append(int(gs.board[6][0]))
    ToReturn.append(int(gs.board[6][1]))
    ToReturn.append(int(gs.board[6][2]))
    ToReturn.append(int(gs.board[6][3]))

    ToReturn.append(int(gs.board[7][0]))
    ToReturn.append(int(gs.board[7][1]))
    ToReturn.append(int(gs.board[7][2]))
    ToReturn.append(int(gs.board[7][3]))

    return ToReturn