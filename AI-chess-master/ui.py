import pygame
import sys
import os

class UserInterface:
    def __init__(self, window, Board):
        self.window = window 
        self.playing = True  
        self.squareSize = 100  
        self.pieces = 64
        self.initialX = 0
        self.initialY = 0       
        self.finalX = 0
        self.finalY = 0
        self.chessboard = Board 
        self.userMove = ""  
        self.aiMove = "" 
        self.userColour = "" 
        self.aiColour = ""
        self.message = ""
        self.font = pygame.font.Font(None, 36)
        self.game_over = False
        self.show_message = False
        self.selected_piece_pos = None
        self.valid_moves = ([], [])
        
        # Sound effects
        self.move_sound = pygame.mixer.Sound("sounds/move.wav") if self.load_sound("sounds/move.wav") else None
        self.capture_sound = pygame.mixer.Sound("sounds/capture.wav") if self.load_sound("sounds/capture.wav") else None

    def load_sound(self, path):
        try:
            return os.path.exists(path)
        except:
            return False

    def displayMessage(self, text):
        try:
            self.message = text
            self.show_message = True
            self.drawBoard()
        except Exception as e:
            print(f"Error displaying message: {str(e)}")

    def handleMove(self):
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False 
                    return
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.initialX = event.pos[0]
                        self.initialY = event.pos[1]
                        x = self.initialY//self.squareSize
                        y = self.initialX//self.squareSize
                        
                        if 0 <= x < 8 and 0 <= y < 8:
                            piece = self.chessboard.board[x][y]
                            if piece.isupper():  # If it's a white piece
                                self.selected_piece_pos = (x, y)
                                self.drawBoard()

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Left click release
                        self.finalX = event.pos[0]
                        self.finalY = event.pos[1]
                        self.selected_piece_pos = None
                        self.calculateMove()
                        
        except Exception as e:
            print(f"Error handling move: {str(e)}")
            self.displayMessage("Error occurred. Please try again.")

    def calculateMove(self):
        try:
            xInitial = self.initialY//self.squareSize
            yInitial = self.initialX//self.squareSize
            xFinal = self.finalY//self.squareSize
            yFinal = self.finalX//self.squareSize
            
            if xInitial < 0 or xInitial > 7 or yInitial < 0 or yInitial > 7 or xFinal < 0 or xFinal > 7 or yFinal < 0 or yFinal > 7:
                self.displayMessage("Move out of board boundaries")
                return
                
            piece = self.chessboard.board[xInitial][yInitial]
            target = self.chessboard.board[xFinal][yFinal]
            
            if not piece.isupper():
                self.displayMessage("Invalid piece to move")
                return
                
            if piece == 'K' and abs(yFinal - yInitial) == 2 and xFinal == xInitial:
                if yInitial == 4:
                    if yFinal == 6 and self.chessboard.board[7][7] == 'R':
                        self.userMove = "7406K"
                    elif yFinal == 2 and self.chessboard.board[7][0] == 'R':
                        self.userMove = "7302K"
            else:
                self.userMove = str(xInitial) + str(yInitial) + str(xFinal) + str(yFinal) + str(target)
                
            if self.userMove in self.chessboard.generateMoveList():
                is_capture = target != '.'
                
                # Play sound
                if is_capture and self.capture_sound:
                    self.capture_sound.play()
                elif self.move_sound:
                    self.move_sound.play()
                    
                self.chessboard.calculateMove(self.userMove)
                self.drawBoard()
                if self.playing:
                    self.aiPlays()
            else:
                self.displayMessage("Invalid or unsafe move")
            
            self.userMove = ""
            self.aiMove = ""
        except Exception as e:
            print(f"Error calculating move: {str(e)}")
            self.displayMessage("Error occurred. Please try again.")

    def drawBoard(self):
        try:
            self.window.fill((255, 255, 255))
            
            # Draw the board squares
            for i in range(0, self.pieces, 2):
                pygame.draw.rect(self.window, (255, 255, 255), 
                               [(i % 8+(i//8) % 2)*self.squareSize, 
                                (i//8)*self.squareSize, 
                                self.squareSize, self.squareSize])
                pygame.draw.rect(self.window, (100, 100, 100), 
                               [((i+1) % 8-((i+1)//8) % 2)*self.squareSize, 
                                ((i+1)//8)*self.squareSize, 
                                self.squareSize, self.squareSize])
            
            # Draw the pieces using image files
            for index in range(self.pieces):
                currentPosition = self.chessboard.board[index//8][index % 8] 
                if currentPosition == "P":
                    chessPieces = pygame.image.load("img/pawn_white.png")
                    chessPieces = pygame.transform.scale(chessPieces, (self.squareSize, self.squareSize)) 
                    self.window.blit(chessPieces, ((index % 8)*self.squareSize, 
                                                 (index//8)*self.squareSize)) 
                elif currentPosition == "p":
                    chessPieces = pygame.image.load("img/pawn_black.png")
                    chessPieces = pygame.transform.scale(chessPieces, (self.squareSize, self.squareSize)) 
                    self.window.blit(chessPieces, ((index % 8)*self.squareSize, 
                                                 (index//8)*self.squareSize)) 
                elif currentPosition == "N":
                    chessPieces = pygame.image.load("img/knight_white.png")
                    chessPieces = pygame.transform.scale(chessPieces, (self.squareSize, self.squareSize)) 
                    self.window.blit(chessPieces, ((index % 8)*self.squareSize, 
                                                 (index//8)*self.squareSize)) 
                elif currentPosition == "n":        
                    chessPieces = pygame.image.load("img/knight_black.png") 
                    chessPieces = pygame.transform.scale(chessPieces, (self.squareSize, self.squareSize)) 
                    self.window.blit(chessPieces, ((index % 8)*self.squareSize, 
                                                 (index//8)*self.squareSize)) 
                elif currentPosition == "B":
                    chessPieces = pygame.image.load("img/bishop_white.png")
                    chessPieces = pygame.transform.scale(chessPieces, (self.squareSize, self.squareSize)) 
                    self.window.blit(chessPieces, ((index % 8)*self.squareSize, 
                                                 (index//8)*self.squareSize)) 
                elif currentPosition == "b":
                    chessPieces = pygame.image.load("img/bishop_black.png")  
                    chessPieces = pygame.transform.scale(chessPieces, (self.squareSize, self.squareSize))  
                    self.window.blit(chessPieces, ((index % 8)*self.squareSize, 
                                                 (index//8)*self.squareSize))           
                elif currentPosition == "R":
                    chessPieces = pygame.image.load("img/rook_white.png") 
                    chessPieces = pygame.transform.scale(chessPieces, (self.squareSize, self.squareSize))  
                    self.window.blit(chessPieces, ((index % 8)*self.squareSize, 
                                                 (index//8)*self.squareSize)) 
                elif currentPosition == "r":
                    chessPieces = pygame.image.load("img/rook_black.png") 
                    chessPieces = pygame.transform.scale(chessPieces, (self.squareSize, self.squareSize))  
                    self.window.blit(chessPieces, ((index % 8)*self.squareSize, 
                                                 (index//8)*self.squareSize))  
                elif currentPosition == "Q":
                    chessPieces = pygame.image.load("img/queen_white.png")  
                    chessPieces = pygame.transform.scale(chessPieces, (self.squareSize, self.squareSize))  
                    self.window.blit(chessPieces, ((index % 8)*self.squareSize, 
                                                 (index//8)*self.squareSize))  
                elif currentPosition == "q":
                    chessPieces = pygame.image.load("img/queen_black.png")
                    chessPieces = pygame.transform.scale(chessPieces, (self.squareSize, self.squareSize))  
                    self.window.blit(chessPieces, ((index % 8)*self.squareSize, 
                                                 (index//8)*self.squareSize))  
                elif currentPosition == "K":
                    chessPieces = pygame.image.load("img/king_white.png") 
                    chessPieces = pygame.transform.scale(chessPieces, (self.squareSize, self.squareSize))  
                    self.window.blit(chessPieces, ((index % 8)*self.squareSize, 
                                                 (index//8)*self.squareSize))  
                elif currentPosition == "k":
                    chessPieces = pygame.image.load("img/king_black.png")  
                    chessPieces = pygame.transform.scale(chessPieces, (self.squareSize, self.squareSize))
                    self.window.blit(chessPieces, ((index % 8)*self.squareSize, 
                                                 (index//8)*self.squareSize))
            
            # Draw message in the middle of the board if there is one
            if self.message and self.show_message:
                s = pygame.Surface((400, 50))
                s.set_alpha(128)
                s.fill((0, 0, 0))
                self.window.blit(s, (200, 375))
                
                text = self.font.render(self.message, True, (0, 255, 0))
                text_rect = text.get_rect(center=(400, 400))
                self.window.blit(text, text_rect)
                    
            pygame.display.update()
        except Exception as e:
            print(f"Error in drawBoard: {str(e)}")
            self.displayMessage("Error occurred. Please try again.")

    def aiPlays(self):
        try:
            if not self.playing:
                return
                
            self.displayMessage("AI Turn")
            pygame.display.update()
            
            self.chessboard.changePlayer()
            self.aiMove = self.chessboard.abPruning(self.chessboard.max_depth, float("inf"), -float("inf"), "", 0)
            
            if not self.playing:
                return
                
            if self.aiMove is None:
                self.displayMessage("CHECKMATE!")
                self.game_over = True
            else:
                is_capture = self.chessboard.board[int(self.aiMove[2])][int(self.aiMove[3])] != '.'
                
                # Play sound for AI moves
                if is_capture and self.capture_sound:
                    self.capture_sound.play()
                elif self.move_sound:
                    self.move_sound.play()
                    
                self.chessboard.calculateMove(self.aiMove)

            self.chessboard.changePlayer()
            self.drawBoard()

            if len(self.chessboard.generateMoveList()) == 0:
                if self.chessboard.isKingSafe() is False:
                    self.displayMessage("CHECKMATE!")
                    self.game_over = True
                else:
                    self.displayMessage("STALEMATE!")
                    self.game_over = True
            elif self.chessboard.isKingSafe() is False:
                self.displayMessage("Check!")
            elif not self.game_over:
                self.displayMessage("Your Turn")
                
        except Exception as e:
            print(f"Error in AI play: {str(e)}")
            if self.playing:
                self.displayMessage("Error occurred. Please try again.")

    def playGame(self):
        try:
            pygame.mixer.init()  # Initialize sound system
            self.userColour = "W"
            self.aiColour = "B"
            self.drawBoard()
            
            while self.playing and not self.game_over:
                try:
                    self.handleMove()
                    pygame.display.update()
                    pygame.time.Clock().tick(60)
                    
                    if self.game_over:
                        pygame.time.wait(3000)
                        break
                        
                except pygame.error:
                    break
                    
        except Exception as e:
            print(f"Error in game loop: {str(e)}")
            
        finally:
            if pygame.get_init():
                try:
                    pygame.quit()
                except:
                    pass