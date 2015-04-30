#!/usr/bin/env python

import copy
import sys
import time

import board
import util

def checkSinglePossibilities(board):
    while True:
        i, j = board.HasSinglePossibility()

        if None == i and None == j:
            break
        else:
            board.Set(i, j, board.GetSinglePossibleValue(i, j))

    print "after filling in single possibilities:"
    board.Display()

def solve(orig, x, y, noDelay):
    board = copy.deepcopy(orig)
    size = board.GetSize()

    possibleValues = [n for n in xrange(1, size)]

    checkSinglePossibilities(board)

    if board.IsSolved():
        return True

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

                    if solve(board, _i, _j, noDelay):
                        return True

                    print str(val) + " at (" + str(i) + ", " + str(j) + ") won't solve, reverting back"
                    try:
                        board.cellPossibilities[i - 1][j - 1].remove(val)
                    except (ValueError):
                        continue

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

        if solve(puzzleFile.GetBoard(), 1, 1, d):
            print "Congratulations!", "the puzzle has been solved!"
        else:
            board = puzzleFile.GetBoard()

            checkSinglePossibilities(board)

            if board.IsSolved():
                print "Congratulations!", "the puzzle has been solved!"
            else:
                print "Sorry!", "the puzzle could not be solved"
                print board.cellPossibilities

    print

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
    else:
        main()