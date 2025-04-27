class pieces:
    def __init__(self, Board):
        self.chessboard = Board
    def move(self, index):
        pass

class Rook(pieces):
    def moveHorizontal(self, row, col, i, potentialmoves):
        count = 1 
        try:
            while(self.chessboard.board[row][col+count*i] == " "):
                previousPosition = self.chessboard.board[row][col+count*i] 
                self.chessboard.board[row][col] = " "
                self.chessboard.board[row][col+count*i] = "R" 
                if self.chessboard.isKingSafe() and col+count*i >= 0:
                    potentialmoves += str(row) + str(col) + str(row) +str(col + count*i) + str(previousPosition)
                self.chessboard.board[row][col] = "R" 
                self.chessboard.board[row][col+count*i] = previousPosition  
                count += 1 
            if self.chessboard.board[row][col+count*i].islower():
                previousPosition = self.chessboard.board[row][col+count*i] 
                self.chessboard.board[row][col] = " "
                self.chessboard.board[row][col+count*i] = "R"  
                if self.chessboard.isKingSafe() and col+count*i >= 0:
                    potentialmoves += str(row) + str(col) + str(row) +str(col + count*i)+str(previousPosition)
                self.chessboard.board[row][col] = "R"  
                self.chessboard.board[row][col+count*i] = previousPosition
        except IndexError:
            pass
        return potentialmoves

    def moveVertical(self, row, col, i, potentialmoves):
        count = 1
        try:
            while(self.chessboard.board[row+count*i][col] == " "):
                previousPosition = self.chessboard.board[row+count*i][col] 
                self.chessboard.board[row][col] = " "  
                self.chessboard.board[row+count*i][col] = "R" 
                if self.chessboard.isKingSafe() and (row+count*i) >=0:
                    potentialmoves += str(row) + str(col) + str(row+count*i) + str(col) + str(previousPosition)
                self.chessboard.board[row][col] = "R" 
                self.chessboard.board[row+count*i][col] = previousPosition
                count += 1 
            if self.chessboard.board[row+count*i][col].islower():
                previousPosition = self.chessboard.board[row+count*i][col] 
                self.chessboard.board[row][col] = " " 
                self.chessboard.board[row+count*i][col] = "R"
                if self.chessboard.isKingSafe() and (row+count*i) >= 0:
                    potentialmoves += str(row) + str(col) + str(row+count*i) + str(col) + str(previousPosition) 
                self.chessboard.board[row][col] = "R" 
                self.chessboard.board[row+count*i][col] = previousPosition 
        except IndexError:
            pass
        return potentialmoves

    def move(self, index):
        potentialmoves = "" 
        row = index//8
        col = index % 8
        for i in [-1,1]:
            potentialmoves = self.moveVertical(row, col, i, potentialmoves)
            potentialmoves = self.moveHorizontal(row, col, i, potentialmoves)
        return potentialmoves


class Knight(pieces):
    def move(self, index):
        potentialmoves = "" 
        row = index//8
        col = index % 8
        for i in [-1,1]:
            for j in [-1,1]:
                try:
                    if self.chessboard.board[row+i][col+j*2] == " " or self.chessboard.board[row+i][col+j*2].islower():
                        previousPosition = self.chessboard.board[row+i][col+j*2]
                        self.chessboard.board[row][col] = " " 
                        self.chessboard.board[row+i][col+j*2] = "N" 
                        if self.chessboard.isKingSafe()and row+i >= 0 and col+j*2 >= 0:
                            potentialmoves += str(row)+str(col) + str(row+i) + str(col+j*2) + str(previousPosition) 
                        self.chessboard.board[row][col] = "N"
                        self.chessboard.board[row+i][col+j*2] = previousPosition
                except IndexError:
                    pass
                try:
                    if self.chessboard.board[row+i*2][col+j] == " " or self.chessboard.board[row+i*2][col+j].islower():
                        previousPosition =self.chessboard.board[row+i*2][col+j] 
                        self.chessboard.board[row][col] = " " 
                        self.chessboard.board[row+i*2][col+j] = "N" 
                        if self.chessboard.isKingSafe() and row+i*2 >= 0 and col+j >=0:
                            potentialmoves += str(row)+str(col) + str(row+i*2) + str(col+j) + str(previousPosition)
                        self.chessboard.board[row][col] = "N"
                        self.chessboard.board[row+i*2][col+j] = previousPosition 
                except IndexError:
                    pass
        return potentialmoves


class Bishop(pieces):
    def moveDiagonal(self, potentialmoves, row, col, i, j):
        count = 1 
        try:
            while(self.chessboard.board[row+count*i][col+count*j] == " "):
                previousPosition = self.chessboard.board[row+count*i][col+count*j] 
                self.chessboard.board[row][col] = " "  
                self.chessboard.board[row+count*i][col+count*j] = "B"  
                if self.chessboard.isKingSafe() and (row+count*i) >=0 and (col+count*j) >= 0:
                    potentialmoves += str(row)+str(col)+str(row+count*i)+str(col+count*j)+str(previousPosition)
                self.chessboard.board[row][col] = "B" 
                self.chessboard.board[row+count*i][col+count*j] = previousPosition 
                count +=1 
            if self.chessboard.board[row+count*i][col+count*j].islower() :
                previousPosition = self.chessboard.board[row+count*i][col+count*j] 
                self.chessboard.board[row][col] = " " 
                self.chessboard.board[row+count*i][col+count*j] = "B"  
                if self.chessboard.isKingSafe() and (row+count*i) >=0 and (col+count*j) >= 0:
                    potentialmoves += str(row)+str(col)+str(row+count*i)+str(col+count*j)+str(previousPosition) 
                self.chessboard.board[row][col] = "B" 
                self.chessboard.board[row+count*i][col+count*j] = previousPosition 
        except IndexError:
            pass
        return potentialmoves


    def move(self, index):
        potentialmoves = "" 
        row = index//8
        col = index % 8
        for i in [-1,1]:
            for j in [-1,1]:
                potentialmoves = self.moveDiagonal(potentialmoves, row, col, i, j)
        return potentialmoves


class Queen(pieces):
    def queenMovement(self, row, col, i, j, potentialmoves):
        count = 1 
        try:
            while(self.chessboard.board[row+count*i][col+count*j] == " "):
                previousPosition = self.chessboard.board[row+count*i][col+count*j]  
                self.chessboard.board[row][col] = " " 
                self.chessboard.board[row+count*i][col+count*j] = "Q"
                if self.chessboard.isKingSafe() and (row+count*i) >=0 and (col+count*j) >= 0:
                    potentialmoves += str(row)+str(col)+str(row+count*i)+str(col+count*j)+str(previousPosition) 
                self.chessboard.board[row][col] = "Q"  
                self.chessboard.board[row+count*i][col+count*j] = previousPosition 
                count += 1
            if self.chessboard.board[row+count*i][col+count*j].islower():
                previousPosition = self.chessboard.board[row+count*i][col+count*j]
                self.chessboard.board[row][col] = " "
                self.chessboard.board[row+count*i][col+count*j] = "Q" 
                if self.chessboard.isKingSafe() and (row+count*i) >=0 and (col+count*j) >= 0:
                    potentialmoves += str(row)+str(col)+str(row+count*i)+str(col+count*j)+str(previousPosition) 
                self.chessboard.board[row][col] = "Q" 
                self.chessboard.board[row+count*i][col+count*j] = previousPosition
        except IndexError:
            pass
        return potentialmoves

    def move(self, index):
        potentialmoves = ""
        row = index//8
        col = index % 8
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                potentialmoves = self.queenMovement(row, col, i, j, potentialmoves)
        return potentialmoves


class King(pieces):
    def kingMovement(self, row, col,index, i, potentialmoves):
        try:
            if self.chessboard.board[row - 1 + i//3][col-1+ i%3].islower() or self.chessboard.board[row - 1 + i//3][col-1+ i%3] == " ":
                previousPosition = self.chessboard.board[row - 1 + i//3][col-1+ i%3] 
                self.chessboard.board[row][col] = " " 
                self.chessboard.board[row - 1 + i//3][col-1+ i%3] = "K" 
                kingTemp = self.chessboard.whiteKing 
                self.chessboard.whiteKing = index+(i//3)*8 +i%3-9
                if self.chessboard.isKingSafe() and row-1+i//3 >=0 and col-1+ i%3>=0:
                        potentialmoves += str(row)+str(col)+str(row-1+i//3)+str(col-1+i%3)+str(previousPosition)
                self.chessboard.board[row][col] = "K" 
                self.chessboard.board[row - 1 + i//3][col-1+ i%3] = previousPosition
                self.chessboard.whiteKing = kingTemp 
        except IndexError:
            pass
        return potentialmoves

    def move(self, index):
        potentialmoves = "" 
        row = index//8
        col = index % 8
        for i in range(9):
            if i != 4:
                potentialmoves = self.kingMovement(row, col,index, i, potentialmoves)
        return potentialmoves


class Pawn(pieces):
    def pawnMovement(self, row, col, index, potentialmoves):
        try:
            if self.chessboard.board[row-1][col] == " " and index >= 16:
                previousPosition = self.chessboard.board[row-1][col]
                self.chessboard.board[row][col] = " " 
                self.chessboard.board[row-1][col] = "P" 
                if self.chessboard.isKingSafe() and (row-1) >= 0:
                    potentialmoves += str(row) + str(col) + str(row-1) + str(col) + str(previousPosition) 
                self.chessboard.board[row][col] = "P"
                self.chessboard.board[row-1][col] = previousPosition
        except IndexError:
            pass
        try:
            if self.chessboard.board[row-1][col] == " " and self.chessboard.board[row-2][col] == " " and index >= 48:
                previousPosition = self.chessboard.board[row-2][col]
                self.chessboard.board[row][col] = " " 
                self.chessboard.board[row-2][col] = "P"
                if self.chessboard.isKingSafe() and row-2 >=0:
                    potentialmoves += str(row) + str(col) + str(row-2) + str(col) + str(previousPosition)
                self.chessboard.board[row][col] = "P"
                self.chessboard.board[row-2][col] = previousPosition  
        except IndexError:
            pass
        return potentialmoves

    def pieceKill(self, row, col, index, potentialmoves):
        for i in [-1,1]:
            try:
                if self.chessboard.board[row-1][col+i].islower():
                    previousPosition = self.chessboard.board[row-1][col+i]
                    self.chessboard.board[row][col] = " " 
                    self.chessboard.board[row-1][col+i] = "P"  
                    if self.chessboard.isKingSafe() and (row-1) >= 0 and (col+i) >= 0:
                        potentialmoves += str(row) + str(col) + str(row-1)+str(col+i) + str(previousPosition)
                    self.chessboard.board[row][col] = "P" 
                    self.chessboard.board[row-1][col+i] = previousPosition  
            except IndexError:
                pass
        return potentialmoves

    def move(self, index):
        potentialmoves = "" 
        row = index//8
        col = index % 8
        potentialmoves = self.pieceKill( row, col,index, potentialmoves)
        potentialmoves = self.pawnMovement(row, col, index, potentialmoves)
        return potentialmoves 