import copy
import sys
import pygame
import random
import numpy as np
import time


WIDTH = 600
HEIGHT = WIDTH
LINE_WIDTH = 15
ROWS = 5
COLS = 5

SQSIZE = WIDTH // COLS
LINE_WIDTH = 15
CIRC_WIDTH = 15
CROSS_WIDTH = 20
RADIUS = SQSIZE // 4
OFFSET = 35  #The space between lines and corners

#Color
CROSS_COLOR = (255, 153, 51)
CIRC_COLOR = (153, 204, 255)
BG_COLOR = (28,170,156)
LINE_COLOR = (23,145, 135)

#Setup Pygame
best_move = None

pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('TIC TAC TOE')
screen.fill( BG_COLOR )

#Global variables:
defaultVal = 0
point = 1
winRule = 4

#Object Class

class Board:

    def __init__(self):
        self.squares = np.zeros( (ROWS, COLS) )
        self.empty_sqrs = self.squares # [squares]
        self.marked_sqrs = 0

    def check_win(self, show = False):
        # Vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] == self.squares[3][col] != 0 or self.squares[4][col] == self.squares[1][col] == self.squares[2][col] == self.squares[3][col] != 0:
                if show:
                    color = (0, 0, 0)
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]

        # Horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] == self.squares[row][3] != 0 or self.squares[row][4] == self.squares[row][1] == self.squares[row][2] == self.squares[row][3] != 0:
                if show:
                    color = (0, 0, 0)
                    iPos = (20, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]

        # Desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] == self.squares[3][3] != 0 or self.squares[4][4] == self.squares[1][1] == self.squares[2][2] == self.squares[3][3] != 0:
            if show:
                color = (0, 0, 0)
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # Asc diagonal
        if self.squares[4][0] == self.squares[3][1] == self.squares[2][2] == self.squares[1][3] != 0 or self.squares[0][4] == self.squares[3][1] == self.squares[2][2] == self.squares[1][3] != 0 :
            if show:
                color = (0, 0, 0)
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # 1st Desc Secondary diagonal
        if self.squares[0][1] == self.squares[1][2] == self.squares[2][3] == self.squares[3][4] != 0:
            if show:
                color = (0, 0, 0)
                iPos = (20 + 120, 20)
                fPos = (600 + 120 -20, 600 - 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]
        
        # 2nd Desc Secondary diagonal
        if self.squares[1][0] == self.squares[2][1] == self.squares[3][2] == self.squares[4][3] != 0:
            if show:
                color = (0, 0, 0)
                iPos = (20,20 + 120)
                fPos = (600 - 20, 600 + 120 - 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # 1st Asc Secondary diagonal
        if self.squares[3][0] == self.squares[2][1] == self.squares[1][2] == self.squares[0][3] != 0:
            if show:
                color = (0, 0, 0)
                iPos = (600 - 120 - 20, 20)
                fPos = (20, 600 - 120 - 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]
        
        # 2nd Asc Secondary diagonal
        if self.squares[4][1] == self.squares[3][2] == self.squares[2][3] == self.squares[1][4] != 0:
            if show:
                color = (0, 0, 0)
                iPos = (120 + 20, 600 - 20)
                fPos = (600 - 20, 120 + 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # Tie condition
        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append( (row, col) )
        
        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 25

    def isempty(self):
        return self.marked_sqrs == 0
    
    def setDefaultHeuristic(self, map):
        for row in range(ROWS):
            for col in range(COLS):
                temp = map[row][col]
                if (temp < defaultVal): continue

                map[row][col]= -2
                map = self.setPointHorizonal(map, (row, col))
                map = self.setPointVertical(map, (row, col))
                map = self.setPointLeftDiagonal(map, (row, col))
                map = self.setPointRightDiagonal(map, (row, col))
                
                map[row][col]= temp + 1
        return map

    def setHeuristic(self,map):
        maze = [[0 for _ in range(len(map))] for _ in range(len(map))]
        maze = self.setDefaultHeuristic(maze)
        for i in range(len(map)):
            for j in range(len(map)):
                if (map[i][j]==1 or map[i][j]==2): maze[i][j]=-map[i][j]

        for i in range(len(maze)):
            for j in range(len(maze)):
                if maze[i][j]>=defaultVal: continue
                maze = self.setPointHorizonal(maze, (i, j))
                maze = self.setPointVertical(maze, (i, j))
                maze = self.setPointLeftDiagonal(maze, (i, j))
                maze = self.setPointRightDiagonal(maze, (i, j))
        return maze

    def setPointRightDiagonal(self,map, pos):
        front = (pos[0]+winRule-1, pos[1]-winRule+1)
        back = (pos[0]-winRule+1, pos[1]+winRule-1)

        bonusPoint = 0
        count=0
        for i, j in zip(range(front[0], back[0]-1, -1), range(front[1], back[1]+1, 1)):
            if (i<0 or i>=len(map) or j<0 or j>=len(map)): continue
            if (map[i][j] >= defaultVal): continue

            if map[i][j] == map[pos[0]][pos[1]]:
                bonusPoint+=2
                count+=1
            else: 
                bonusPoint+=1

        for i, j in zip(range(front[0], back[0]-1, -1), range(front[1], back[1]+1, 1)):
            if (i<0 or i>=(ROWS) or j<0 or j>=(COLS)): continue

            if map[i][j]<defaultVal and map[i][j]!= map[pos[0]][pos[1]]:
                return map
            if (map[i][j] < defaultVal): continue
            map[i][j]+=point+bonusPoint+count
        return map

    def setPointLeftDiagonal(self,map, pos):
        front = (pos[0]-winRule+1, pos[1]-winRule+1)
        back = (pos[0]+winRule-1, pos[1]+winRule-1)

        bonusPoint = 0
        count = 0
        for i, j in zip(range(front[0], back[0]+1), range(front[1], back[1]+1)):
            if (i<0 or i>=len(map) or j<0 or j>=len(map)): continue
            if map[i][j] >= defaultVal: continue
       
            if map[i][j] == map[pos[0]][pos[1]]:
                bonusPoint+=2
                count+=1
            else: 
                bonusPoint+=1


        for i, j in zip(range(front[0], back[0]+1), range(front[1], back[1]+1)):
            if (i<0 or i>=len(map) or j<0 or j>=len(map)): continue
        
            if map[i][j] < defaultVal and map[i][j]!= map[pos[0]][pos[1]]:
                return map
            if map[i][j] < defaultVal: continue
            map[i][j]+=point+bonusPoint+count
        return map

    def setPointHorizonal(self,map, pos):
        front = pos[1]-winRule+1
        if (front<=0): front=0
        back = pos[1]+winRule-1
        if (back>=(ROWS)): back = (ROWS)-1

        bonusPoint = 0
        count = 0
        for i in range(front, back+1):
            if map[pos[0]][i]>=defaultVal: continue
       
            if map[pos[0]][i] == map[pos[0]][pos[1]]:
                bonusPoint+=2
                count+=1
            else: 
                bonusPoint+=1

        for i in range(front, back+1):
            if map[pos[0]][i]<defaultVal and map[pos[0]][i] != map[pos[0]][pos[1]]:
                return map
            if map[pos[0]][i]<defaultVal: continue
            map[pos[0]][i] += point+bonusPoint+count
        return map

    def setPointVertical(self,map, pos):
        front = pos[0]-winRule+1
        if (front<=0): front=0
        back = pos[0]+winRule-1
        if (back>=COLS): back = COLS-1

        bonusPoint = 0
        count = 0
        for i in range(front, back+1):
            if map[pos[0]][i]>=defaultVal: continue
            if map[pos[0]][i] == map[pos[0]][pos[1]]:
                bonusPoint+=2
                count+=1
            else: 
                bonusPoint+=1

    
        for i in range(front, back+1):
            
            if map[i][pos[1]]<defaultVal and map[i][pos[1]]!= map[pos[0]][pos[1]]:
                return map
            if map[i][pos[1]]<defaultVal: continue
            map[i][pos[1]]+=point+bonusPoint+count
        return map
    
    def getMax(self,map):
     
        map = self.setHeuristic(map)
        max = -10000
        move = tuple()
        for i in range(ROWS):
            for j in range(COLS):
                if (map[i][j]>=defaultVal and map[i][j]>max and map[i][j] != self.isempty):
                    max = map[i][j]
                    move = (i, j)
        return move

class AI:

    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    # --- RANDOM ---

    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx] # (row, col)

    def minimax(self,board, maximizing, depth):
        
        case = board.check_win()
        # player 1 wins
        if case == 1:
            return 1, None # eval, move

        # player 2 wins
        if case == 2:
            return -1, None

        # draw
        elif board.isfull() or depth == 0:
            return 0, None
 
        maze = board.setHeuristic(board.squares)
        mazeHeuristic = []
        maxVal = 0
        for i in range (len(maze)):
            for j in range (len(maze)):
                if maze[i][j] > maxVal:
                    mazeHeuristic = []
                    mazeHeuristic.append([i,j])
                    maxVal = maze[i][j]
                if maxVal == maze[i][j]:
                    mazeHeuristic.append([i,j])

        
                
        # for item in (maze):
        #     print (item)


        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = mazeHeuristic

            for tempArray in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(tempArray[0],tempArray[1], 1)
                finalEval = self.minimax(temp_board, False, depth - 1)[0]
                if finalEval > max_eval:
                    max_eval = finalEval
                    best_move = (tempArray[0],tempArray[1])
                # alpha = max(alpha, finalEval)
                # if (beta <= alpha):
                #     break
            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = mazeHeuristic

            for tempArray in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(tempArray[0], tempArray[1], self.player)
                finalEval = self.minimax(temp_board, True, depth - 1)[0]
                if finalEval < min_eval:
                    min_eval = finalEval
                    best_move = (tempArray[0], tempArray[1])
                # beta = min(beta, finalEval)
                # if beta <= alpha:
                #     break
            return min_eval, best_move  

    # --- MAIN EVAL ---

    def eval(self, main_board):
        temp_map = [[val for val in row] for row in main_board.squares]
        start = time.time()
        if self.level != 0:
            # minimax algo choice
            move = self.minimax(main_board, False, 4)[1]
            # if(move == None):
            #     move = main_board.getMax(temp_map)
            #     for row in (main_board.squares):
            #         print(row)

        print(f'AI has chosen to mark the square in pos {move} ')
        print(f'Time calculation: {time.time()- start}')
        return move # row, col


class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1   #1-cross  #2-circles
        self.gamemode = 'ai' 
        self.running = True
        self.show_lines()

    #Drawing functions

    def show_lines(self):
        # bg
        screen.fill( BG_COLOR )

        # vertical
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (2*SQSIZE, 0), (2*SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (3*SQSIZE, 0), (3*SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        # horizontal
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - 3*SQSIZE), (WIDTH, HEIGHT - 3*SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - 2*SQSIZE), (WIDTH, HEIGHT - 2*SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            # draw cross
            # desc line
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
            # asc line
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)
        
        elif self.player == 2:
            # draw circle
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

    # --- OTHER METHODS ---

    def make_move(self, row, col):
        self.board.squares[row][col] = self.player
        self.draw_fig(row, col)
        self.next_turn()

    def next_turn(self):
        self.player = self.player % 2 + 1

    def isover(self):
        return self.board.check_win(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()

def main():
    game = Game()
    board = game.board
    ai = game.ai

    #Main loop
    while True:
        
        # pygame events
        for event in pygame.event.get():

            # quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # keydown event
            if event.type == pygame.KEYDOWN:

                # r-restart - Press R to restart the game
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

            # click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE
                
                # human mark sqr
                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)

                    if game.isover():
                        game.running = False


        # AI initial call
        if game.gamemode == 'ai' and game.player == ai.player and game.running:

            # update the screen
            pygame.display.update()

            # eval
            row, col = ai.eval(board)
            # board.squares[row][col]  = 2
            game.make_move(row, col)
           

            if game.isover():
                game.running = False
            
        pygame.display.update()

main()