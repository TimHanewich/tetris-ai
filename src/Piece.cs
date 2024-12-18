using System;

namespace Tetris
{
    public class Piece
    {
        public bool[,] Squares {get; set;}

        public Piece()
        {
            Squares = new bool[2,2];
        }

        public static Piece CreateRandom()
        {
            //Construct random
            Piece ToReturn = new Piece();
            Random r = new Random();
            int selection = r.Next(0, 7); //Pick at random: 0,1,2,3,4,5,6

            if (selection == 0)
            {
                ToReturn.Squares[0,0] = true;
                ToReturn.Squares[1,0] = false;
                ToReturn.Squares[0,1] = false;
                ToReturn.Squares[1,1] = false;
            }
            else if (selection == 1)
            {
                ToReturn.Squares[0,0] = true;
                ToReturn.Squares[1,0] = false;
                ToReturn.Squares[0,1] = true;
                ToReturn.Squares[1,1] = false;
            }
            else if (selection == 2)
            {
                ToReturn.Squares[0,0] = true;
                ToReturn.Squares[1,0] = true;
                ToReturn.Squares[0,1] = false;
                ToReturn.Squares[1,1] = false;
            }
            else if (selection == 3)
            {
                ToReturn.Squares[0,0] = true;
                ToReturn.Squares[1,0] = true;
                ToReturn.Squares[0,1] = true;
                ToReturn.Squares[1,1] = false;
            }
            else if (selection == 4)
            {
                ToReturn.Squares[0,0] = true;
                ToReturn.Squares[1,0] = false;
                ToReturn.Squares[0,1] = true;
                ToReturn.Squares[1,1] = true;
            }
            else if (selection == 5)
            {
                ToReturn.Squares[0,0] = true;
                ToReturn.Squares[1,0] = true;
                ToReturn.Squares[0,1] = false;
                ToReturn.Squares[1,1] = true;
            }
            else if (selection == 6)
            {
                ToReturn.Squares[0,0] = false;
                ToReturn.Squares[1,0] = true;
                ToReturn.Squares[0,1] = true;
                ToReturn.Squares[1,1] = true;
            }

            return ToReturn;
        }

        public override string ToString()
        {
            string ToReturn = "--" + "\n";
            for (int r = 0; r < 2; r++)
            {
                for (int c = 0; c < 2; c++)
                {
                    if (Squares[r,c])
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
            ToReturn = ToReturn + "--";
            return ToReturn;
        }

        private static bool OddsOf(float odds)
        {
            Random r = new Random();
            return r.NextSingle() < odds;
        }

        
    }
}