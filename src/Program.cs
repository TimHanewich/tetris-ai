using System;

namespace Tetris
{
    public class Program
    {
        public static void Main(string[] args)
        {
            while (true)
            {
                Piece p = Piece.CreateRandom();
                Console.WriteLine(p);
                Console.ReadLine();
            }
        }
    }
}