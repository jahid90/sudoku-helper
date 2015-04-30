#!/usr/bin/env python

import sys
import time

import board
import util

def solve(puzzleFile, x, y):
    board = puzzleFile.GetBoard()
    size = board.GetSize()

    possibleValues = [n for n in xrange(1, size)]

    for i in xrange(x, size):
        for j in xrange(y, size):
            if 0 == board.Get(i, j):
                for val in possibleValues:
                    time.sleep(1)

                    print "attempting with", val, "at (", i, ", ", j, ")"

                    board.Set(i, j, val)

                    if 0 == board.Get(i, j):
                        print "can't proceed, rules violation"
                        continue

                    print "board configuration at this stage:"
                    board.Display()

                    _i = i
                    _j = (j + 1) % size

                    if 0 == _j:
                        _j = 1
                        _i = (i + 1) % size

                    if 0 == _i:
                        return board.IsSolved()

                    if solve(puzzleFile, _i, _j):
                        return True

                    print val, "at (", i, ", ", j, ") won't solve, revertng back"
                    board.Unset(i, j)


    return False

def usage():
    progName = sys.argv[0][sys.argv[0].rfind('/') + 1 : ]
    params = " <file_with_sudoku_puzzle>"
    usage = "usage: " + progName +  params

    print usage

def main():
    puzzleFile = util.PuzzleFile(sys.argv[1])

    puzzleFile.Read()
    puzzleFile.Parse()

    if solve(puzzleFile, 1, 1):
        print "Congratulations!", "the puzzle has been solved!"
        puzzleFile.GetBoard().Display()
    else:
        print "Sorry!", "the puzzle could not be solved"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
    else:
        main()