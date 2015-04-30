#!/usr/bin/env python

import sys

class Board():
    def __init__(self, size = 3):
        self.separatorDist = size
        self.size = size * size + 1

        self.grid = []

        self.rowExclusions = []
        self.columnExclusions = []
        for i in xrange(0, self.size):
            self.rowExclusions.append([])
            self.columnExclusions.append([])

        self.maxRowExcl = 0
        self.maxColExcl = 0

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

    def GetSize(self):
        return self.size

    def Set(self, x, y, val):
        if not (0 < x < self.size and 0 < y < self.size):
            print "Error!", "cell indices must be between 1 and", self.size - 1

        elif not 0 == self.grid[x][y]:
            print "Error!", "cell already contains a value"

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

            self.maxRowExcl = max(self.maxRowExcl, len(self.rowExclusions[x]))
            self.maxColExcl = max(self.maxColExcl, len(self.columnExclusions[y]))

            self.rowExclusions[x].sort()
            self.columnExclusions[y].sort()

    def Unset(self, x, y):
        val = self.grid[x][y]

        if not 0 == val:
            self.grid[x][y] = 0

            self.rowExclusions[x].remove(val)
            self.columnExclusions[y].remove(val)

            # TODO reset maxRowExcl and maxColExcl count
            # entry could have been removed from row/col with max entries

    def Get(self, x, y):
        if not (0 < x < self.size and 0 < y < self.size):
            self.rangeError()
        else:
            return self.grid[x][y]

    def CheckRowValid(self):
        for i in xrange(1, self.size):
            row = []
            for j in xrange(1, self.size):
                val = self.grid[i][j]
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
                val = self.grid[j][i]
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
                val = self.grid[i][j]
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
                    sys.stdout.write("Warning! mini square (" + str(i + 1) + ", " + str(j + 1) + ") ")
                    return False

        return True

    def IsSolved(self):
        for i in xrange(1, self.size):
            for j in xrange(1, self.size):
                if 0 == self.grid[i][j]:
                    return False

        return True


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
            for j in xrange(0, self.maxRowExcl):
                if j < len(self.rowExclusions[i]):
                    sys.stdout.write(str(self.rowExclusions[i][j]) + " ")

            print

            if 0 == i % self.separatorDist and i < self.size:
                print "--" * (self.size + (1 + self.size / self.separatorDist) + self.maxRowExcl)

        # print the colun exclusions
        for i in xrange(0, self.maxColExcl):
            for j in xrange(0, self.size):
                if i < len(self.columnExclusions[j]):
                    sys.stdout.write(str(self.columnExclusions[j][i]) + " ")
                else:
                    sys.stdout.write("  ")

                if 0 == j % self.separatorDist and j < self.size:
                    sys.stdout.write("| ")
            print

        print
