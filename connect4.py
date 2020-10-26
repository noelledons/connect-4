import numpy as np      
import pygame
import sys
import math

#RGB VALUES
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
PINK = (255, 51, 153)

#Board Functions
ROW_COUNT = 6
COLUMN_COUNT = 7
def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT -1][col] == 0 #Column has empty slot

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0: #If the slot is still 0, then it's empty
            return r

def print_board(board): #Changes the orientation of the board
    print(np.flip(board, 0))

def winning_move(board, piece):
    #Check horizontal locations for win
    for c in range(COLUMN_COUNT -3): 
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    #Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    #Check positively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    #Check negatively sloped diagonals
    for c in range( COLUMN_COUNT -3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] ==1: #player 1 drops a circle
                    pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2),height -int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2: #player 2 drops a circle
                    pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height -int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

board = create_board()
print_board(board) #- Board, with selection option
game_over = False #Becomes true when a player has 4 in a row
turn = 0

#Visuals
pygame.init()

SQUARESIZE = 80 #100 pixels

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("roboto",90)
pygame.display.set_caption('Connect 4')

#Information about Player 1 and Player 2
while not game_over:

    for event in pygame.event.get(): #Motions
        if event.type == pygame.QUIT: #Exit
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE)) #Black space at the top
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))  #To get rid of the circle at the end of the game
            #Ask for Player 1 input
            if turn == 0:  
                posx = event.pos[0]
                col= int(math.floor(posx/SQUARESIZE)) 
                if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winning_move(board, 1):
                            label= myfont.render("Player 1 wins!! :)", 1, RED)
                            screen.blit(label, (40,10))
                            game_over = True

            #Ask for Player 2 input
            else:
                posx = event.pos[0]
                col= int(math.floor(posx/SQUARESIZE))
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        label= myfont.render("Player 2 wins!! :)", 2, YELLOW)
                        screen.blit(label, (40,10))
                        game_over = True

            print_board(board)
            draw_board(board)

            turn +=1
            turn = turn % 2 #Alternates between player 1 and 2's turn

            if game_over:
                pygame.time.wait(3000) #Game will close in 3 seconds
