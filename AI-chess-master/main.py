import pygame
import sys
from board import Board
from ui import UserInterface

def selectDifficulty():
    try:
        pygame.init()
        screen = pygame.display.set_mode([400, 300])
        pygame.display.set_caption('Select Difficulty')
        
        # Colors
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        GRAY = (200, 200, 200)
        GREEN = (0, 255, 0)
        
        # Font
        font = pygame.font.Font(None, 36)
        
        # Button dimensions
        button_width = 200
        button_height = 50
        button_margin = 20
        
        # Create buttons
        buttons = [
            {"text": "EASY", "rect": pygame.Rect(100, 100, button_width, button_height)},
            {"text": "MEDIUM", "rect": pygame.Rect(100, 170, button_width, button_height)},
            {"text": "HARD", "rect": pygame.Rect(100, 240, button_width, button_height)}
        ]
        
        # Title
        title = font.render("Select Difficulty Level", True, BLACK)
        title_rect = title.get_rect(center=(200, 50))
        
        difficulty = None
        running = True
        
        while running:
            screen.fill(WHITE)
            screen.blit(title, title_rect)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for button in buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            if button["text"] == "EASY":
                                difficulty = 2
                            elif button["text"] == "MEDIUM":
                                difficulty = 3
                            elif button["text"] == "HARD":
                                difficulty = 4
                            running = False
            
            # Draw buttons
            for button in buttons:
                pygame.draw.rect(screen, GRAY, button["rect"])
                pygame.draw.rect(screen, BLACK, button["rect"], 2)
                text = font.render(button["text"], True, BLACK)
                text_rect = text.get_rect(center=button["rect"].center)
                screen.blit(text, text_rect)
            
            pygame.display.flip()
            pygame.time.Clock().tick(60)
        
        return difficulty
    except Exception as e:
        print(f"Error in difficulty selection: {str(e)}")
        return None

def main():
    try:
        # Get difficulty level
        difficulty = selectDifficulty()
        if difficulty is None:
            return
            
        # Initialize game window with standard size
        window = pygame.display.set_mode([800, 800])
        pygame.display.set_caption('AI Chess')
        
        # Initialize game with selected difficulty
        board = Board()
        board.max_depth = difficulty
        UI = UserInterface(window, board)
        UI.playGame()
        
    except Exception as e:
        print(f"Error in main game: {str(e)}")
    finally:
        try:
            pygame.quit()
        except:
            pass

if __name__ == "__main__":
    main()
