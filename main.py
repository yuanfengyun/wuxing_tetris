import pygame
import sys
import random

pygame.init()
width = 16
hight = 32
screen = pygame.display.set_mode((320,640))
font =  pygame.font.SysFont('microsoft Yahei',60)
surface = font.render('火',False,(255,200,10))

fcclock = pygame.time.Clock()

map = []
cur_cube = [2,3,30]
down_clock = 0
color_tbl = [
    [0,0,0],
    [255,215,0],     #金
    [0,255,0],       #木
    [255,255,255],   #水
    [255,0,0],       #火
    [255,160,122]    #土
]

kill_tbl = [0,2,5,4,1,3]
birth_tbl = [0,3,4,2,5,1]

def init_map():
    for i in range(0,hight):
        row = []
        for j in range(0,width):
            row.append(0)
        map.append(row)

def draw_map():
    for i in range(0,hight):
        for j in range(0,width):
            obj = map[i][j]
            pygame.draw.rect(screen,color_tbl[obj],[j*20,(hight-i-1)*20,18,18],1)
    if cur_cube[0] > 0:
        pygame.draw.rect(screen,color_tbl[cur_cube[0]],[cur_cube[1]*20,(hight - cur_cube[2]-1)*20,18,18],1)
#        screen.blit(surface,(cur_cube[1]*20,(hight - cur_cube[2]-1)*20))

def gen_cube():
    cur_cube[0] = random.randint(1,5)
    cur_cube[1] = 3
    cur_cube[2] = 30

def valid_gride(x,y):
    if x < 0 or x >= width:
        return False

    if y < 0 or y >= hight:
        return False

    return True

def move(dir):
    if cur_cube[0] == 0:
        return

    if dir == "left":
        if cur_cube[1] < 1:
            return
        if map[cur_cube[2]][cur_cube[1]-1] >0:
            return
        cur_cube[1] = cur_cube[1] - 1

    if dir == "right":
        if cur_cube[1] >= width-1:
            return
        if map[cur_cube[2]][cur_cube[1]+1] > 0:
            return
        cur_cube[1] = cur_cube[1] + 1

#被克，直接消失
def calc_be_kill():
    remove_list = []
    for y in range(0,hight):
        for x in range(0,width):
            cur = map[y][x]
            if cur == 0:
                continue
            if valid_gride(x-1,y) and kill_tbl[map[y][x-1]] == cur:
                remove_list.append([x,y])
            if valid_gride(x+1,y) and kill_tbl[map[y][x+1]] == cur:
                remove_list.append([x,y])
            if valid_gride(y-1,y) and kill_tbl[map[y-1][x]] == cur:
                remove_list.append([x,y])
            if valid_gride(y+1,y) and kill_tbl[map[y+1][x]] == cur:
                remove_list.append([x,y])
            
    for v in remove_list:
        map[v[1]][v[0]] = 0

speed_up = False
def move_down():
    if speed_up == False and down_clock % 4 > 0:
        return

    if speed_up == True and down_clock % 2 > 0:
        return

    if cur_cube[0] == 0:
        return

    if cur_cube[2] < 1:
        return

    if map[cur_cube[2]-1][cur_cube[1]] > 0:
        map[cur_cube[2]][cur_cube[1]]=cur_cube[0]
        calc_be_kill()
        gen_cube()
        return

    cur_cube[2] = cur_cube[2] - 1
    if cur_cube[2] == 0:
        map[cur_cube[2]][cur_cube[1]]=cur_cube[0]
        calc_be_kill()
        gen_cube()

init_map()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == 275:
                move("right")
            if event.key == 276:
                move("left")
            if event.key == 274:
                speed_up = True
        if event.type == pygame.KEYUP:
            if event.key == 274:
                speed_up = False
    move_down()
    draw_map()

    fcclock.tick(40)
    down_clock = down_clock + 1
    pygame.display.update()

pygame.quit()
    
    