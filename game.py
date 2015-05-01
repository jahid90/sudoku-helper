#!/usr/bin/env python

import copy
import sys
import time

import board
import util

def checkAndFillSinglePossibilities(board):

    while True:
        i, j = board.HasSinglePossibility()
    
        if board.IsDebug():
            board.Display()
            print
            print board.PrintPossibilityMatrix()
            print
            print "next single possibility at", util.Helper().PointsToString(i, j)

        if None == i and None == j:
            break
        else:
            retVal = board.FillSinglePossibility(i, j)

            if -1 == retVal:
                sys.exit(-1)

    print
    print "after filling in single possibilities:"
    board.Display()

    if board.IsDebug():
        print
        print board.PrintPossibilityMatrix()
        print

def tryWith(val, i, j, board, noDelay):
    size = board.GetSize()

    if not noDelay:
        time.sleep(2)

    print "attempting with " + str(val) + " at (" + str(i) +  ", " + str(j) + ")"

    board.Set(i, j, val)

    board.Display()

    if 0 == board.Get(i, j):
        print "can't proceed, rules violation"
        #continue
        return False

    _i = i
    _j = (j + 1) % size

    if 0 == _j:
        _j = 1
        _i = (i + 1) % size

    if 0 == _i:
        return board.IsSolved()

    if solve(board, _i, _j, noDelay):
        return True

    print str(val), "at", util.Helper().PointsToString(i, j), "won't solve, reverting back"
    #try:
        #board.cellPossibilities[i - 1][j - 1].remove(val)
    board.RemovePossibility(i, j, val)
    checkAndFillSinglePossibilities(board)
    #except (ValueError):
        #return False

    board.Unset(i, j)

    return False

def solve(orig, x, y, noDelay):
    board = copy.deepcopy(orig)
    size = board.GetSize()

    possibleValues = [n for n in xrange(1, size)]

    checkAndFillSinglePossibilities(board)

    if board.IsSolved():
        return True

    for i in xrange(x, size):
        for j in xrange(y, size):
            if 0 == board.Get(i, j):
                if board.IsDebug():
                    print "board configuration at this stage:"
                    board.Display()

                for val in board.GetPossibleValues(i, j):
                    retVal = tryWith(val, i, j, board, noDelay)

                    if retVal:
                        return True

    return False

def usage():
    progName = sys.argv[0][sys.argv[0].rfind('/') + 1 : ]
    params = " <file_with_sudoku_puzzle>"
    options = " [OPTionsS]"

    optDetails = """
OPTS
    --solve         attempt to solve the puzzle
    --no-delay      do not pause between steps
    --debug         enable debug messages
    """

    usage = "usage: " + progName + options + params

    print usage
    print optDetails

def main():
    path = sys.argv[len(sys.argv) - 1]

    attemptToSolve = False
    noDelay = False
    debug = False

    if not 0 == sys.argv.count('--solve'):
        attemptToSolve = True

    if not 0 == sys.argv.count('--no-delay'):
        noDelay = True

    if not 0 == sys.argv.count('--debug'):
        debug = True

    puzzleFile = util.PuzzleFile(path)

    puzzleFile.Read()
    puzzleFile.Parse()

    puzzleFile.GetBoard().SetDebug(debug)

    if debug:
        print puzzleFile.GetBoard().PrintPossibilityMatrix()
        print

    if attemptToSolve:
        print

        if solve(puzzleFile.GetBoard(), 1, 1, noDelay):
            print "Congratulations!", "the puzzle has been solved!"
        else:
            board = puzzleFile.GetBoard()

            #checkAndFillSinglePossibilities(board)

            if board.IsSolved():
                print "Congratulations!", "the puzzle has been solved!"
            else:
                print "Sorry!", "the puzzle could not be solved"
                #print board.cellPossibilities

    print

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
    else:
        main()