#!/usr/bin/env python

import sys

import util

class Board():
    def __init__(self, size = 3):
        self.separatorDist = size
        self.size = size * size + 1

        self.debug = False
        self.invertExcl = False

        self.grid = []

        self.rowExclusions = []
        self.columnExclusions = []

        self._initExcl()

        self._initGrid()        

        self._initCellPossibilities()

    def _initExcl(self):
        for i in xrange(0, self.size):
            self.rowExclusions.append([])
            self.columnExclusions.append([])

    def _initGrid(self):
        headerRow = []
        for i in xrange(0, self.size):
            headerRow.append(i)

        self.grid.append(headerRow)

        for i in xrange(1, self.size):
            row = []
            row.append(i)
            for j in xrange(1, self.size):
                row.append(0)
            self.grid.append(row)

    def _initCellPossibilities(self):
        self.cellPossibilities = [[[x for x in xrange(1, self.size)] for y in xrange(1, self.size)] for z in xrange(1, self.size)]

    def GetSize(self):
        return self.size

    def Set(self, x, y, val):
        if not (0 < x < self.size and 0 < y < self.size):
            print "Error!", "cell indices must be between 1 and", self.size - 1

        elif not 0 == self.grid[x][y]:
            print "Error!", "cell (" + str(x) + ", " + str(y) + ") already contains a value"

        else:
            self.grid[x][y] = val

            #if False == self.CheckRowValid():
            if not 0 == self.rowExclusions[x].count(val):
                print "Warning!", "row:", x, "cannot contain more than one", val
                self.grid[x][y] = 0
                return

            #if False == self.CheckColValid():
            if not 0 == self.columnExclusions[y].count(val):
                print "Warning!", "col:", y, "cannot contain more than one", val
                self.grid[x][y] = 0
                return

            if False == self.CheckAllMiniSquares():
                print "cannot contain more than one", val
                self.grid[x][y] = 0
                return

            self.rowExclusions[x].append(val)
            self.columnExclusions[y].append(val)

            self.rowExclusions[x].sort()
            self.columnExclusions[y].sort()

            self.RemovePossibilities(x, y, val)

    def Unset(self, x, y):
        val = self.Get(x, y)

        if not 0 == val:
            self.grid[x][y] = 0

            self.rowExclusions[x].remove(val)
            self.columnExclusions[y].remove(val)

            self.AddPossibilities(x, y, val)

    def Get(self, x, y):
        if not (0 < x < self.size and 0 < y < self.size):
            self.rangeError()
        else:
            return self.grid[x][y]

    def GetPossibleValues(self, x, y):
        return self.cellPossibilities[x - 1][y - 1]

    def ResetPossibility(self, x, y):
        self.cellPossibilities[x - 1][y - 1] = []

        if self.debug:
            print "resetting possibility list for", util.Helper().PointsToString(x, y)

    def RemovePossibility(self, x, y, val):
        try:
            self.cellPossibilities[x - 1][y - 1].remove(val)

            if self.debug:
                print "removing", str(val), "as possibility for", util.Helper().PointsToString(x, y)
        except (ValueError):
            return

    def RemovePossibilities(self, x, y, val):
        if self.debug:
            print "setting", str(val), "at", util.Helper().PointsToString(x, y)

        self.ResetPossibility(x, y)

        for i in xrange(1, self.size):
            self.RemovePossibility(i, y, val)

        for j in xrange(1, self.size):
            self.RemovePossibility(x, j, val)

        cellX = (x - 1) // self.separatorDist
        cellY = (y - 1) // self.separatorDist

        for i in xrange(1 + self.separatorDist * cellX, 1 + self.separatorDist * (cellX + 1)):
            for j in xrange(1 + self.separatorDist * cellY, 1 + self.separatorDist * (cellY + 1)):
                self.RemovePossibility(i, j, val)

    def AddPossibility(self, x, y, val):
        if not 0 == self.Get(x, y):
            if self.debug:
                print "already filled; cannot add", str(val), "as possibility for", util.Helper().PointsToString(x, y)

            return

        if 0 == self.cellPossibilities[x - 1][y - 1].count(val):
            self.cellPossibilities[x - 1][y - 1].append(val)

            if self.debug:
                print "adding", str(val), "as possibility for", util.Helper().PointsToString(x, y)

    def NotInMiniSquare(self, val, x, y):
        cellX = (x - 1) // self.separatorDist
        cellY = (y - 1) // self.separatorDist

        for i in xrange(1 + self.separatorDist * cellX, 1 + self.separatorDist * (cellX + 1)):
            for j in xrange(1 + self.separatorDist * cellY, 1 + self.separatorDist * (cellY + 1)):
                if val == self.Get(i, j):
                    return False

        return True

    def AddPossibilities(self, x, y, val):
        for i in xrange(1, self.size):
            if self.NotInMiniSquare(val, i, y):
                self.AddPossibility(i, y, val)

        for j in xrange(1, self.size):
            if self.NotInMiniSquare(val, i, y):
                self.AddPossibility(x, j, val)

        cellX = (x - 1) // self.separatorDist
        cellY = (y - 1) // self.separatorDist

        for i in xrange(1 + self.separatorDist * cellX, 1 + self.separatorDist * (cellX + 1)):
            for j in xrange(1 + self.separatorDist * cellY, 1 + self.separatorDist * (cellY + 1)):
                if self.NotInMiniSquare(val, i, y):
                    self.AddPossibility(i, j, val)

        for i in xrange(1, self.size):
            self.AddPossibility(x, y, i)

        for i in self.rowExclusions[x]:
            self.RemovePossibility(x, y, i)

        for j in self.columnExclusions[y]:
            self.RemovePossibility(x, y, j)

        for i in xrange(1 + self.separatorDist * cellX, 1 + self.separatorDist * (cellX + 1)):
            for j in xrange(1 + self.separatorDist * cellY, 1 + self.separatorDist * (cellY + 1)):
                if not 0 == self.Get(i, j):
                    self.RemovePossibility(x, y, self.Get(i, j))


    def HasSinglePossibility(self):
        for i in xrange(1, self.size):
            for j in xrange(1, self.size):
                if 1 == len(self.cellPossibilities[i - 1][j - 1]):
                    if 0 == self.Get(i, j):
                        return i, j
                    else:
                        self.RemovePossibility(i, j, self.Get(i, j))

        return None, None

    def FillSinglePossibility(self, x, y):
        val = self.GetSinglePossibleValue(x, y)

        if not 1 == len(val):
            print "Error!", "cell (" + str(x) + ", " + str(y) + ") does not have single possible value"
            return 1

        if 0 == self.Get(x, y):
            self.Set(x, y, val[0])

        if 0 == self.Get(x, y):
            print "Error!", "rules not fulfilled"
            return -1

        return 0

    def GetSinglePossibleValue(self, x, y):
        if not 1 == len(self.cellPossibilities[x - 1][y - 1]):
            message = "(" + str(x) + ", " + str(y) + ") does not have single possibility"
            raise RuntimeError(message)

        return self.cellPossibilities[x - 1][y - 1]

    def CheckRowValid(self):
        for i in xrange(1, self.size):
            row = []
            for j in xrange(1, self.size):
                val = self.Get(i, j)
                if not 0 == val:
                    if not 0 == row.count(val):
                        return False
                    else:
                        row.append(val)
        return True

    def CheckColValid(self):
        for i in xrange(1, self.size):
            row = []
            for j in xrange(1, self.size):
                val = self.Get(j, i)
                if not 0 == val:
                    if not 0 == row.count(val):
                        return False
                    else:
                        row.append(val)
        return True

    def CheckMiniSquareValid(self, r, c):
        mini = []
        for i in xrange(1 + self.separatorDist * r, 1 + self.separatorDist * (r + 1)):
            for j in xrange(1 + self.separatorDist * c, 1 + self.separatorDist * (c + 1)):
                val = self.Get(i, j)
                if not 0 == val:
                    if not 0 == mini.count(val):
                        return False
                    else:
                        mini.append(val)
        return True

    def CheckAllMiniSquares(self):
        retVal = True
        for i in xrange(0, self.separatorDist):
            for j in xrange(0, self.separatorDist):
                retVal = self.CheckMiniSquareValid(i, j)

                if False == retVal:
                    sys.stdout.write("Warning! mini square " + util.Helper.PointsToString(i, j) + " is not valid")
                    return False

        return True

    def IsSolved(self):
        for i in xrange(1, self.size):
            for j in xrange(1, self.size):
                if 0 == self.Get(i, j):
                    return False

        print "***" * 2 * self.GetSize()
        self.Display()
        print "***" * 2 * self.GetSize()

        return True

    def SetInvertExcl(self, invertExcl):
        self.invertExcl = invertExcl

    def GetInverseExcl(self, type, idx):
        if 0 == idx:
            return []

        if "row" == type:
            r = [x for x in xrange(1, self.GetSize())]

            for i in self.rowExclusions[idx]:
                r.remove(i)

            return r

        if "col" == type:
            c = [x for x in xrange(1, self.GetSize())]

            for i in self.columnExclusions[idx]:
                c.remove(i)

            return c

        return None

    def SetDebug(self, state):
        self.debug = state

    def IsDebug(self):
        return self.debug

    def PrintPossibilityMatrix(self):
        for i in xrange(0, self.size - 1):
            for j in xrange(0, self.size - 1):
                if not 0 == len(self.cellPossibilities[i][j]):
                    print util.Helper().PointsToString(i + 1, j + 1), ":", self.cellPossibilities[i][j]

    def PrintExclusions(self):
        print "rows"
        for i in xrange(1, self.GetSize()):
            print i, ":", self.rowExclusions[i]

        print "cols"
        for j in xrange(1, self.GetSize()):
            print j, ":", self.columnExclusions[j]

    def Display(self):
        print

        for i in xrange(0, self.size):
            for j in xrange(0, self.size):
                val = self.grid[i][j]

                if 0 == val:
                    val = "  "
                else:
                    val = str(val) + " "

                sys.stdout.write(val)

                if 0 == j % self.separatorDist and j < self.size:
                    sys.stdout.write("| ")

            # print the row exclusions
            if self.invertExcl:
                r = self.GetInverseExcl("row", i)
            else:
                r = self.rowExclusions[i]

            for j in xrange(0, self.size - 1):
                if not 0 == r.count(j + 1):
                    sys.stdout.write(str(j + 1) + " ")
                else:
                    sys.stdout.write("  ")

            print

            if 0 == i % self.separatorDist and i < self.size:
                print "--" * (self.size + (1 + self.size / self.separatorDist) + (self.size - 1))

        # print the column exclusions
        for i in xrange(0, self.size - 1):
            for j in xrange(0, self.size):
                if self.invertExcl:
                    c = self.GetInverseExcl("col", j)
                else:
                    c = self.columnExclusions[j]

                #if i < len(self.columnExclusions[j]):
                    #sys.stdout.write(str(self.columnExclusions[j][i]) + " ")
                if not 0 == c.count(i + 1):
                    sys.stdout.write(str(i + 1) + " ")
                else:
                    sys.stdout.write("  ")

                if 0 == j % self.separatorDist and j < self.size:
                    sys.stdout.write("| ")
            print

        print
