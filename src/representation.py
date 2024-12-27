import tetris

def PieceState(p:tetris.Piece) -> list[int]:
    ToReturn:list[int] = []
    for r in range(0, len(p.squares)):
        for c in range(0, len(p.squares[r])):
            ToReturn.append(int(p.squares[r][c]))
    return ToReturn
    

def BoardState(gs:tetris.GameState) -> list[int]:
    """Returns the state of the board, expressed as the relative depths of each column available"""
    coldepths:list[int] = gs.column_depths()
    while 0 not in coldepths:
        for i in range(0, len(coldepths)):
            coldepths[i] = coldepths[i] - 1
    return coldepths