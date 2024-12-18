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
            for (int r = 0; r < 2; r++)
            {
                for (int c = 0; c < 2; c++)
                {
                    ToReturn.Squares[r,c] = OddsOf(0.5f);
                }
            }

            //First, look for bad patterns
            //Ensure it is not one of these: https://i.imgur.com/YE4VKdc.png
            if (ToReturn.Squares[0,0] == false && ToReturn.Squares[1,0] == true && ToReturn.Squares[0,1] == true && ToReturn.Squares[1,1] == false)
            {
                if (OddsOf(0.5f))
                {
                    ToReturn.Squares[0,0] = true;
                }
                else
                {
                    ToReturn.Squares[1,1] = true;
                }
            }
            else if (ToReturn.Squares[0,0] == true && ToReturn.Squares[1,0] == false && ToReturn.Squares[0,1] == false && ToReturn.Squares[1,1] == true) //Ensure it is not one of these: https://i.imgur.com/YE4VKdc.png
            {
                if (OddsOf(0.5f))
                {
                    ToReturn.Squares[1,0] = true;
                }
                else
                {
                    ToReturn.Squares[0,1] = true;
                }
            }

            //If there is only one, put it in top left
            int NumberOccupied = 0;
            for (int r = 0; r < 2; r++)
            {
                for (int c = 0; c < 2; c++)
                {
                    if (ToReturn.Squares[r,c])
                    {
                        NumberOccupied = NumberOccupied + 1;
                    }
                }
            }

            //Handle different scenarios
            if (NumberOccupied == 0) //There are none
            {
                ToReturn.Squares[0,0] = true; //put one on
            }
            if (NumberOccupied == 1) //If there is only one, ensure it is the top one
            {
                ToReturn.Squares[0,0] = true;
                ToReturn.Squares[1,0] = false;
                ToReturn.Squares[0,1] = false;
                ToReturn.Squares[1,1] = false;
            }
            else if (NumberOccupied == 4) //If all are on, turn one random one off
            {
                if (OddsOf(0.5f))
                {
                    if (OddsOf(0.5f))
                    {
                        ToReturn.Squares[0,0] = false;
                    }
                    else
                    {
                        ToReturn.Squares[1,0] = false;
                    }
                }
                else
                {
                    if (OddsOf(0.5f))
                    {
                        ToReturn.Squares[0,1] = false;
                    }
                    else
                    {
                        ToReturn.Squares[1,1] = false;
                    }
                }
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