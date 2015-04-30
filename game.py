#!/usr/bin/env python

import sys
import time

import board
import util

def solve(puzzleFile, x, y, noDelay):
    board = puzzleFile.GetBoard()
    size = board.GetSize()

    possibleValues = [n for n in xrange(1, size)]

    for i in xrange(x, size):
        for j in xrange(y, size):
            if 0 == board.Get(i, j):
                for val in possibleValues:
                    if not noDelay:
                        time.sleep(1)

                    print "attempting with " + str(val) + " at (" + str(i) +  ", " + str(j) + ")"

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

                    if solve(puzzleFile, _i, _j, noDelay):
                        return True

                    print val, "at (", i, ", ", j, ") won't solve, revertng back"
                    board.Unset(i, j)


    return False

def usage():
    progName = sys.argv[0][sys.argv[0].rfind('/') + 1 : ]
    params = " <file_with_sudoku_puzzle>"
    options = " [OPTS]"

    optDetails = """
OPTS
    --solve         attempt to solve the puzzle
    --no-delay      do not pause between steps
    """

    usage = "usage: " + progName + options + params

    print usage
    print optDetails

def main():
    path = sys.argv[len(sys.argv) - 1]

    s = False
    d = False

    if not 0 == sys.argv.count('--solve'):
        s = True

    if not 0 == sys.argv.count('--no-delay'):
        d = True

    puzzleFile = util.PuzzleFile(path)

    puzzleFile.Read()
    puzzleFile.Parse()

    if s:
        print
        puzzleFile.GetBoard().Display()

        if solve(puzzleFile, 1, 1, d):
            print "Congratulations!", "the puzzle has been solved!"
        else:
            print "Sorry!", "the puzzle could not be solved"

    print

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
    else:
        main()