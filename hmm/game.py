import pygame
from .board import Board

import random
from datetime import datetime

import math

pygame.init()
random.seed(datetime.now())

from .constants import HEIGHT, WIDTH, BLACK, YELLOW1, YELLOW2, RED, GRAY, GREEN, ORANGE

fx = [0, 0, 1, -1, -1, 1, 1, -1]
fy = [1, -1, 0, 0, 1, 1, -1, -1]

hv_2 = 0.48
ang_2 = 0.036
slf_2 = 0.004

hv_3 = 0.32
ang_3 = 0.018
slf_3 = 0.004

hv_4 = 0.24
ang_4 = 0.009
slf_4 = 0.004

# RED=1, ORANGE=2, GREEN=3
dict = {

    (1,1):1.0,
    (1,2):0.00,
    (1,3):0.00,

    (2,1):0.00,
    (2,2):1.0,
    (2,3):0.00,

    (3,1):0.00,
    (3,2):0.00,
    (3,3):1.0,
}


 
class Game:
    def __init__(self, win, rows, cols):
        self.win = win
        self.rows = rows
        self.cols = cols
        self.row_size = HEIGHT // (rows+1)
        self.col_size = WIDTH // cols

        self.prob =  [[0.0 for col in range(cols)] for row in range(rows)] 
        self.cell_clr =  [[BLACK for col in range(cols)] for row in range(rows)] 
        self.cell_clr1 = [[BLACK for col in range(cols)] for row in range(rows)] 

        self.ghost_r = random.randint(0, rows-1)
        self.ghost_c = random.randint(0, cols-1)

        self.red_dis = 0
        self.org_dis = 0
        self.grn_dis = 0

        self.catch = 0


        self.board = Board(win, rows, cols)
        self.init()

    
    def init(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if row % 2 == 0:
                    if col % 2 == 0:
                        self.cell_clr[row][col] = YELLOW1
                        self.cell_clr1[row][col] = YELLOW1     
                    else:
                        self.cell_clr[row][col] = YELLOW2
                        self.cell_clr1[row][col] = YELLOW2         
                else:
                    if col % 2 == 0:
                        self.cell_clr[row][col] = YELLOW2
                        self.cell_clr1[row][col] = YELLOW2       
                    else:
                        self.cell_clr[row][col] = YELLOW1
                        self.cell_clr1[row][col] = YELLOW1
                self.prob[row][col] =  1 / (self.rows * self.cols)

        dis = self.rows + self.cols - 2

        self.red_dis = 2
        dis -=  2
        self.org_dis = self.red_dis + math.ceil(dis/2)
        dis -= math.ceil(dis/2)
        self.grn_dis = self.org_dis + dis

        self.win.fill(BLACK)
        self.board.draw_time_catch()
        self.show_prob()
        
  

    def update_board_clr(self, clr):
        for row in range(self.rows):
            for col in range(self.cols):
                self.board.draw_rect(row, col, clr[row][col])
                   

    def refresh(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.cell_clr[row][col] = self.cell_clr1[row][col]

        self.update_board_clr(self.cell_clr)
        self.board.clr_res()

     
    def normalize(self):
        tot = 0.0  
        for row in range(self.rows):
            for col in range(self.cols):
                tot += self.prob[row][col]
        if tot == 0:
            print("error")
            return
        for row in range(self.rows):
            for col in range(self.cols):
                self.prob[row][col] = self.prob[row][col]/tot 
        


    def show_prob(self):
        self.update_board_clr(self.cell_clr)
        for row in range(self.rows):
            for col in range(self.cols):
                self.board.draw_prob(row, col, self.prob[row][col])
         
  

    def cell_type(self, row, col):
        cnt = 0
        for i in range(4):
            tx = row + fx[i]
            ty = col + fy[i]
            if 0<=tx<self.rows and 0<=ty<self.cols:
                cnt += 1
        return cnt

    def get_time_transition_prob(self, row, col, flag):   
        c_type = self.cell_type(row, col)
        if c_type == 2:
            if flag == 0:
                return self.prob[row][col]*hv_2
            else:
                return self.prob[row][col]*ang_2
        elif c_type == 3:
            if flag == 0:
                return self.prob[row][col]*hv_3
            else:
                return self.prob[row][col]*ang_3
        else:
            if flag == 0:
                return self.prob[row][col]*hv_4
            else:
                return self.prob[row][col]*ang_4


    def calc_prob(self, row, col):
        ret = 0.0
        for i in range(8):
            tx = row + fx[i]
            ty = col + fy[i]
            if 0<=tx<self.rows and 0<=ty<self.cols:
                if i < 4:
                    ret += self.get_time_transition_prob(tx, ty, 0)
                else:
                    ret += self.get_time_transition_prob(tx, ty, 1)

        c_type = self.cell_type(row, col)
        if c_type == 2:
            ret += self.prob[row][col]*slf_2
        elif c_type == 3:
            ret += self.prob[row][col]*slf_3
        else:
            ret += self.prob[row][col]*slf_4
        
        return ret

    def set_ghost_pos(self, flag, where):
        cnt = 0
        if flag == 0:
            for i in range(4):
                tx = self.ghost_r + fx[i]
                ty = self.ghost_c + fy[i]
                if 0<=tx<self.rows and 0<=ty<self.cols:
                    cnt += 1
                if cnt == where:
                    self.ghost_r = tx
                    self.ghost_c = ty
                    return
        else:
            for i in range(4, 8):
                tx = self.ghost_r + fx[i]
                ty = self.ghost_c + fy[i]
                if 0<=tx<self.rows and 0<=ty<self.cols:
                    cnt += 1
                if cnt == where:
                    self.ghost_r = tx
                    self.ghost_c = ty
                    return



    def handle_ghost_two(self, prob):
        if prob <= hv_2:
            self.set_ghost_pos(0,1)
        elif prob <= hv_2 * 2.0:
            self.set_ghost_pos(0,2)
        elif prob <= hv_2 * 2.0 + ang_2:
            self.set_ghost_pos(1,1)

    def handle_ghost_three(self, prob):
        if prob <= hv_3:
            self.set_ghost_pos(0,1)
        elif prob <= hv_3 * 2.0:
            self.set_ghost_pos(0,2)
        elif prob <= hv_3 * 3.0:
            self.set_ghost_pos(0,3)
        elif prob <= hv_3 * 3.0 + ang_2:
            self.set_ghost_pos(1,1)
        elif prob <= hv_3 * 3.0 + ang_2 * 2.0:
            self.set_ghost_pos(1,2)

    def handle_ghost_four(self, prob):
        if prob <= hv_4:
            self.set_ghost_pos(0,1)
        elif prob <= hv_4 * 2.0:
            self.set_ghost_pos(0,2)
        elif prob <= hv_4 * 3.0:
            self.set_ghost_pos(0,3)
        elif prob <= hv_4 * 4.0:
            self.set_ghost_pos(0,4)
        elif prob <= hv_4 * 4.0 + ang_4:
            self.set_ghost_pos(1,1)
        elif prob <= hv_4 * 4.0 + ang_4 * 2.0: 
            self.set_ghost_pos(1,2)
        elif prob <= hv_4 * 4.0 + ang_4 * 3.0:  
            self.set_ghost_pos(1,3)
        elif prob <= hv_4 * 4.0 + ang_4 * 4.0:  
            self.set_ghost_pos(1,4)



    def update_ghost_pos(self):
        c_type = self.cell_type(self.ghost_r, self.ghost_c)
        prob = random.random()

        if c_type == 2:
            self.handle_ghost_two(prob)
        elif c_type == 3:
            self.handle_ghost_three(prob)
        else:
            self.handle_ghost_four(prob)
            

    def handle_time_advance(self):
        prob =  [[0.0 for col in range(self.cols)] for row in range(self.rows)] 
        for row in range(self.rows):
            for col in range(self.cols):
                prob[row][col] =  self.calc_prob(row, col)
        
        for row in range(self.rows):
            for col in range(self.cols):
                self.prob[row][col] = prob[row][col]
        self.update_ghost_pos()


    def update_evidence_prob(self, row, col, clr):
        x = 0
        if clr == RED:
            x = 1
        elif clr == ORANGE:
            x = 2
        else:
            x = 3
        for r in range(self.rows):
            for c in range(self.cols):
                dis = abs(row - r) + abs(col - c)
                if dis <= self.red_dis:
                    self.prob[r][c] = self.prob[r][c] * dict[(1,x)]
                elif dis <= self.org_dis:
                    self.prob[r][c] = self.prob[r][c] * dict[(2,x)]
                else:
                    self.prob[r][c] = self.prob[r][c] * dict[(3,x)]           
        self.normalize()


    def handle_evidence(self, row, col):
        cur_dis = abs(row - self.ghost_r) + abs(col - self.ghost_c)
        prob = random.random()

        if cur_dis <= self.red_dis:
            if prob <= 1.0:
                self.cell_clr[row][col] = RED
            elif prob <= 0.95 + 0.03:
                self.cell_clr[row][col] = ORANGE
            else:
                self.cell_clr[row][col] = GREEN    
        elif cur_dis <= self.org_dis:
            if prob <= 1.0:
                self.cell_clr[row][col] = ORANGE
            elif prob <= 0.90 + 0.05:
                self.cell_clr[row][col] = RED
            else:
                self.cell_clr[row][col] = GREEN   
        else:
            if prob <= 1.0:
                self.cell_clr[row][col] = GREEN
            elif prob <= 0.95 + 0.03:
                self.cell_clr[row][col] = ORANGE
            else:
                self.cell_clr[row][col] = RED 

        self.update_evidence_prob(row, col, self.cell_clr[row][col])


    def reveal_ghost(self, row, col):
        if row == self.ghost_r and col == self.ghost_c:
            print("GHOST COUGHT")
            self.board.show_result("CAUGHT")
        else:
            print("MISSED")
            self.board.show_result("MISSED")
        
        self.cell_clr[self.ghost_r][self.ghost_c] = GRAY


                
    def handle_click(self, row, col):
        if 0<=row<self.rows and 0<=col<self.cols:
            if self.catch == 0:
                self.refresh()
                self.handle_evidence(row, col)
            else:
                self.refresh()
                self.reveal_ghost(row, col)
                self.catch = 0
                
        elif row == self.rows and col == 0:
            self.handle_time_advance()
            self.refresh()
            self.catch = 0
        elif row == self.rows and col == self.cols-1:
            self.catch = 1
            self.refresh()
 