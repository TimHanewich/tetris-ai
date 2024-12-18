using System;
using System.Diagnostics;

namespace Tetris
{
    public struct GameState
    {
        public bool[,] Board;

        public GameState()
        {
            Board = new bool[8,4]; //8 rows, 4 columns
        }

        public override string ToString()
        {
            string ToReturn = "";

            ToReturn = "----" + "\n";
            for (int r = 0; r < 8; r++)
            {
                for (int c = 0; c < 4; c++)
                {
                    if (Board[r,c])
                    {
                        ToReturn = ToReturn + "X";
                    }
                    else
                    {
                        ToReturn = ToReturn + " ";
                    }
                }
                ToReturn = ToReturn + "\n";
            }
            ToReturn = ToReturn + "----";

            return ToReturn;
        }

        public void Drop(Piece p, int shift)
        {
            if (shift < 0 || shift > 3)
            {
                throw new Exception("Shift must be between 0 and 3.");
            }

            
        }
    }
}