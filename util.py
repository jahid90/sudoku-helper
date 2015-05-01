#!/usr/bin/env python

import board

class PuzzleFile():
    def __init__(self, filename):
        self.filename = filename[filename.rfind('/') + 1 : ]
        self.dirname = filename[ : filename.rfind('/') + 1]

        self.lines = None

        self.board = None

    def Read(self):
        with open(self.dirname + self.filename) as f:
            self.lines = [line.rstrip() for line in f]

    def Parse(self):
        size = int(self.lines[0])

        self.board = board.Board(size)

        for i in xrange(0, size * size):
            row = self.lines[i + 1].split()
            for j in xrange(0, size * size):
                if not '0' == row[j]:
                    self.board.Set(i + 1, j + 1, int(row[j]))

        print "successfully parsed file", self.filename
        self.board.Display()

    def GetBoard(self):
        return self.board

class Helper():
    def CheckZero(self, arg):
        return 0 == arg

    def CheckOne(self, arg):
        return 1 == arg

    def PointsToString(self, x, y):
        return "(" + str(x) + ", " + str(y) + ")"
        