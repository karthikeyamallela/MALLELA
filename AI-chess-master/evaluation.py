from piece import *

class Evaluation:
    def __init__(self, Board):
        self.evaluation = 0
        self.material = 0
        self.chessboard = Board 


    def finalEvaluation(self, numberofMoves, depth):
        self.evaluation += self.materialEvaluation()+self.safetyEvaluation()+self.positionEvaluation(numberofMoves,depth,self.material) 
        self.chessboard.changePlayer()  
        self.material = self.materialEvaluation()
        self.evaluation -= self.materialEvaluation()-self.safetyEvaluation()-self.positionEvaluation(numberofMoves,depth,self.material)
        self.chessboard.changePlayer()  
        return -(self.evaluation + depth*60)


    def materialEvaluation(self):
        materialEvaluation = 0 
        bishopCounter = 0  
        for index in range(self.chessboard.total_piece):
            piece = self.chessboard.board[index//8][index % 8]
            if piece == "P":
                materialEvaluation += 100  
            elif piece == "N":
                materialEvaluation += 400 
            elif piece == "R":
                materialEvaluation += 600  
            elif piece == "B":
                bishopCounter += 1 
            elif piece == "Q":
                materialEvaluation += 1200 
        if bishopCounter >= 2:
            materialEvaluation += 200*bishopCounter  
        elif bishopCounter == 1:
            materialEvaluation += 150 

        return materialEvaluation

    def safetyEvaluation(self):
        safetyEvaluation = 0
        temporyKingPosition = self.chessboard.whiteKing
        for i in range(self.chessboard.total_piece):
            piece = self.chessboard.board[i//8][i%8]
            if piece == "P":
                self.whiteKing = i 
                if self.chessboard.isKingSafe() is False:
                    safetyEvaluation -= 50
            elif piece == "N":
                self.whiteKing = i  
                if self.chessboard.isKingSafe() is False:
                    safetyEvaluation -= 150
            elif piece == "B":
                self.whiteKing = i 
                if self.chessboard.isKingSafe() is False:
                    safetyEvaluation -= 150
            elif piece == "R":
                self.whiteKing = i 
                if self.chessboard.isKingSafe() is False:
                    safetyEvaluation -= 300
            elif piece == "Q":
                self.whiteKing = i 
                if self.chessboard.isKingSafe() is False:
                    safetyEvaluation -= 450
        self.chessboard.whiteKing = temporyKingPosition
        if (self.chessboard.isKingSafe() is False):
            safetyEvaluation -= 500
        return safetyEvaluation

    def positionEvaluation(self, numberofMoves, depth, material):
        positionEvaluation = numberofMoves  
        if numberofMoves == 0:
            if self.chessboard.isKingSafe() is False:
                positionEvaluation += -(200000*depth)
            else:
                positionEvaluation += -(150000*depth) 
        return positionEvaluation