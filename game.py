#!/usr/bin/env python

import copy
import sys

import board
import util

def checkAndFillSinglePossibilities(board):

    while True:
        i, j = board.HasSinglePossibility()
    
        if board.IsDebug():
            board.Display()
            print
            board.PrintPossibilityMatrix()
            print
            print "next single possibility at", util.Helper().PointsToString(i, j)

        if None == i and None == j:
            break
        else:
            retVal = board.FillSinglePossibility(i, j)

            if -1 == retVal:
                if board.IsDebug():
                    print "this branch won't result in solution"

                return

    print
    print "after filling in single possibilities:"
    board.Display()

    if board.IsDebug():
        print
        board.PrintPossibilityMatrix()
        print

def tryWith(val, i, j, board, noDelay):
    _board = copy.deepcopy(board)

    size = board.GetSize()

    if not noDelay:
        import time
        time.sleep(2)

    print "attempting with " + str(val) + " at (" + str(i) +  ", " + str(j) + ")"

    _board.Set(i, j, val)

    if 0 == _board.Get(i, j):
        print "can't proceed, rules violation"
        return False

    _board.Display()

    checkAndFillSinglePossibilities(_board)

    if _board.IsSolved():
        return True

    _i = i
    _j = (j + 1) % size

    if 0 == _j:
        _j = 1
        _i = (i + 1) % size

    if 0 == _i:
        return _board.IsSolved()

    # find the next cell to check for; checkAndFillSinglePossibilities
    # could have already filled in the cell we were going to try for
    while not 0 == _board.Get(_i, _j):
        _j = (_j + 1) % size

        if 0 == _j:
            _j = 1
            _i = (_i + 1) % size

        if 0 == _i:
            return _board.IsSolved()

    if solve(_board, _i, _j, noDelay):
        return True

    print str(val), "at", util.Helper().PointsToString(i, j), "won't solve"

    board.RemovePossibility(i, j, val)

    checkAndFillSinglePossibilities(board)

    if board.IsSolved():
        return True

    return False

def checkIfPreviousCellsEmpty(board, x, y):
    for i in xrange(1, x):
        for j in xrange(1, board.GetSize()):
            if 0 == board.Get(i, j):
                return True

    for j in xrange(1, y):
        if 0 == board.Get(x, j):
            return True

    return False

def solve(orig, x, y, noDelay):
    board = copy.deepcopy(orig)
    size = board.GetSize()

    if checkIfPreviousCellsEmpty(board, x, y):
        if board.IsDebug():
            print "previous cells are empty; this branch won't solve"

        return

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
                    print
                    board.PrintPossibilityMatrix()
                    print

                for val in board.GetPossibleValues(i, j):
                    if checkIfPreviousCellsEmpty(board, i, j):
                        if board.IsDebug():
                            print "previous cells are empty; this branch won't solve"

                        break

                    retVal = tryWith(val, i, j, board, noDelay)

                    if retVal:
                        return True

    return False

def usage():
    progName = sys.argv[0][sys.argv[0].rfind('/') + 1 : ]
    params = " <file_with_sudoku_puzzle>"
    options = " [OPTIONS]"

    optDetails = """
OPTIONS
    --solve         attempt to solve the puzzle
    --no-delay      do not pause between steps
    --debug         enable debug messages
    --invert-excl   display possibilities instead of entries already filled in
    --help          display this help and exit
    """

    usage = "usage: " + progName + options + params

    print usage
    print optDetails

def main():
    path = sys.argv[len(sys.argv) - 1]

    attemptToSolve = False
    noDelay = False
    debug = False
    invertExcl = False

    if not 0 == sys.argv.count('--solve'):
        attemptToSolve = True

    if not 0 == sys.argv.count('--no-delay'):
        noDelay = True

    if not 0 == sys.argv.count('--debug'):
        debug = True

    if not 0 == sys.argv.count('--invert-excl'):
        invertExcl = True

    puzzleFile = util.PuzzleFile(path)

    puzzleFile.Read()
    puzzleFile.Parse()

    puzzleFile.GetBoard().SetDebug(debug)
    puzzleFile.GetBoard().SetInvertExcl(invertExcl)

    print "successfully parsed file", path
    puzzleFile.GetBoard().Display()

    if debug:
        puzzleFile.GetBoard().PrintPossibilityMatrix()
        print


    if attemptToSolve:
        print

        if solve(puzzleFile.GetBoard(), 1, 1, noDelay):
            print "Congratulations!", "the puzzle has been solved!"
        else:
            print "Sorry!", "the puzzle could not be solved"

    print

if __name__ == '__main__':
    if len(sys.argv) < 2 or not 0 == sys.argv.count('--help'):
        usage()
    else:
        main()