from evaluation import Evaluation
import piece

class Board:
    def __init__(self):
        self.board = [
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", "Q", "K", "B", "N", "R"]
        ]
        self.total_piece = 64
        self.whiteKing = 60 
        self.blackKing = 4  
        self.max_depth = 3  


    def generateMoveList(self):
        moves = "" 
        rook = piece.Rook(self)
        knight = piece.Knight(self)
        bishop = piece.Bishop(self)
        queen = piece.Queen(self)
        king = piece.King(self)
        pawn = piece.Pawn(self)
        for index in range(self.total_piece):
            currentPosition = self.board[index//8][index%8]
            if currentPosition == 'R':
                moves += rook.move(index)
            elif currentPosition == 'N':
                moves += knight.move(index)
            elif currentPosition == 'B':
                moves += bishop.move(index)
            elif currentPosition == 'Q':
                moves += queen.move(index)
            elif currentPosition == 'K':
                moves += king.move(index) 
            elif currentPosition == 'P':
                moves += pawn.move(index)
        return moves

    def isKingSafe(self):
        kingXpos = self.whiteKing//8
        kingYpos = self.whiteKing % 8
        
        # Check for knight attacks
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                try:
                    if self.board[kingXpos + i][kingYpos + 2*j] == "n" and kingXpos + i >= 0 and kingYpos + 2*j >= 0:
                        return False
                except IndexError:
                    continue
                try:
                    if self.board[kingXpos + 2*i][kingYpos + j] == "n" and kingXpos + 2*i >= 0 and kingYpos + j >= 0:
                        return False
                except IndexError:
                    continue
                    
        # Check for king attacks
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                try:
                    if self.board[kingXpos + i][kingYpos + j] == "k" and kingXpos + i >= 0 and kingYpos + j >= 0:
                        return False
                except IndexError:
                    continue
                    
        # Check for pawn attacks
        if kingXpos > 0:
            try:
                if self.board[kingXpos - 1][kingYpos - 1] == "p" and kingYpos - 1 >= 0:
                    return False
            except IndexError:
                pass
            try:
                if self.board[kingXpos - 1][kingYpos + 1] == "p" and kingYpos + 1 < 8:
                    return False
            except IndexError:
                pass
                
        # Check for rook and queen attacks (horizontal and vertical)
        for i in range(-1, 2, 2):
            # Horizontal check
            for j in range(1, 8):
                try:
                    if self.board[kingXpos][kingYpos + j*i] == " ":
                        continue
                    if self.board[kingXpos][kingYpos + j*i] in ["r", "q"] and kingYpos + j*i >= 0:
                        return False
                    break
                except IndexError:
                    break
                    
            # Vertical check
            for j in range(1, 8):
                try:
                    if self.board[kingXpos + j*i][kingYpos] == " ":
                        continue
                    if self.board[kingXpos + j*i][kingYpos] in ["r", "q"] and kingXpos + j*i >= 0:
                        return False
                    break
                except IndexError:
                    break
                    
        # Check for bishop and queen attacks (diagonal)
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                for k in range(1, 8):
                    try:
                        if self.board[kingXpos + k*i][kingYpos + k*j] == " ":
                            continue
                        if self.board[kingXpos + k*i][kingYpos + k*j] in ["b", "q"] and kingXpos + k*i >= 0 and kingYpos + k*j >= 0:
                            return False
                        break
                    except IndexError:
                        break
                        
        return True

    def calculateMove(self, move):
        if move[4] == "P" or move[4] == "C":
            if move[4] == "P":
                self.board[1][int(move[0])] = " " 
                self.board[0][int(move[1])] = move[3]
            elif move[4] == "C":
                self.board[7][int(move[0])] = " "
                self.board[7][int(move[1])] = "K"
                self.board[7][int(move[2])] = move[3] 

        else:
            self.board[int(move[2])][int(move[3])] = self.board[int(move[0])][int(move[1])] 
            self.board[int(move[0])][int(move[1])] = " " 
            if self.board[int(move[2])][int(move[3])] == "K":
                self.whiteKing = 8*(int(move[2]))+int(move[3])



    def rollbackMove(self, move):
        if move[4] == "P" or move[4] == "C":
            if move[4] == "P":
                self.board[1][int(move[0])] = "P" 
                self.board[0][int(move[1])] = move[2]  
            elif move[4] == "C":
                self.board[7][int(move[1])] = " "
                self.board[7][int(move[2])] = "K"
                self.board[7][int(move[0])] = move[3]
        else:
            self.board[int(move[0])][int(move[1])] = self.board[int(move[2])][int(move[3])]
            self.board[int(move[2])][int(move[3])] = move[4] 
            if self.board[int(move[0])][int(move[1])] == "K":
                self.whiteKing = 8*int(move[0])+int(move[1]) 




    def abPruning(self, depth, beta, alpha, move, maximizingPlayer):
        potentialmoves = self.generateMoveList()
        evaluation = Evaluation(self)
        if depth == 0 or len(potentialmoves) == 0:
            if move == "":
                return None
            else:
                return move + str(evaluation.finalEvaluation(len(potentialmoves), depth)*(maximizingPlayer*2-1))

        maximizingPlayer = 1 - maximizingPlayer
        for i in range(0, len(potentialmoves), 5):
            self.calculateMove(potentialmoves[i:(i+5)])
            self.changePlayer()
            nextNode = self.abPruning(depth-1, beta, alpha, potentialmoves[i:(i+5)], maximizingPlayer)  
            value = int(nextNode[5:])
            self.changePlayer()
            self.rollbackMove(potentialmoves[i:(i+5)])
            if maximizingPlayer == 0:
                if value <= beta:
                    beta = value 
                    if depth == self.max_depth:
                        move = nextNode[0:5] 
            else:
                if value > alpha:
                    alpha = value 
                    if depth == self.max_depth:
                        move = nextNode[0:5]
                if alpha >= beta:
                    if maximizingPlayer == 0:
                        return move + str(beta) 
                    else:
                        return move + str(alpha) 
        if maximizingPlayer == 0:
            return move + str(beta) 
        else:
            return move + str(alpha)

    def changePlayer(self):
        for index in range(32):
            row = index//8
            column = index % 8
            if self.board[row][column].isupper():
                flippiece = self.board[row][column].lower()
            else:
                flippiece = self.board[row][column].upper()  
            if self.board[7-row][7-column].isupper():
                self.board[row][column] = self.board[7-row][7-column].lower()
            else:
                self.board[row][column] = self.board[7-row][7-column].upper()  
            self.board[7-row][7-column] = flippiece 
        kingFlipped = self.whiteKing
        self.whiteKing = 63 - self.blackKing
        self.blackKing = 63 - kingFlipped