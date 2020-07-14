import math
import pygame
import random
import tkinter as tk
from tkinter import messagebox
pygame.init()
win=pygame.display.set_mode((500,500))
win.fill((255,255,255))

class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 40)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False
def redrawwindow():
    win.fill((255,255,255))
    BG.draw(win,(0,0,0))
    SG.draw(win,(0,0,0))
    PG.draw(win,(0,0,0))
def Block_Game():
    pygame.font.init()

    s_width = 800
    s_height = 700
    play_width = 300 
    play_height = 600 
    block_size = 30
    top_left_x = (s_width - play_width) // 2
    top_left_y = s_height - play_height

    S = [['.....',
        '.....',
        '..00.',
        '.00..',
        '.....'],
        ['.....',
        '..0..',
        '..00.',
        '...0.',
        '.....']]
    Z = [['.....',
        '.....',
        '.00..',
        '..00.',
        '.....'],
        ['.....',
        '..0..',
        '.00..',
        '.0...',
        '.....']]
    I = [['..0..',
        '..0..',
        '..0..',
        '..0..',
        '.....'],
        ['.....',
        '0000.',
        '.....',
        '.....',
        '.....']]
    O = [['.....',
        '.....',
        '.00..',
        '.00..',
        '.....']]
    J = [['.....',
        '.0...',
        '.000.',
        '.....',
        '.....'],
        ['.....',
        '..00.',
        '..0..',
        '..0..',
        '.....'],
        ['.....',
        '.....',
        '.000.',
        '...0.',
        '.....'],
        ['.....',
        '..0..',
        '..0..',
        '.00..',
        '.....']]
    L = [['.....',
        '...0.',
        '.000.',
        '.....',
        '.....'],
        ['.....',
        '..0..',
        '..0..',
        '..00.',
        '.....'],
        ['.....',
        '.....',
        '.000.',
        '.0...',
        '.....'],
        ['.....',
        '.00..',
        '..0..',
        '..0..',
        '.....']] 
    T = [['.....',
        '..0..',
        '.000.',
        '.....',
        '.....'],
        ['.....',
        '..0..',
        '..00.',
        '..0..',
        '.....'],
        ['.....',
        '.....',
        '.000.',
        '..0..',
        '.....'],
        ['.....',
        '..0..',
        '.00..',
        '..0..',
        '.....']]
    
    shapes = [S, Z, I, O, J, L, T]
    shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

    class Piece(object):
        rows = 20 
        columns = 10 

        def __init__(self, column, row, shape):
            self.x = column
            self.y = row
            self.shape = shape
            self.color = shape_colors[shapes.index(shape)]
            self.rotation = 0

    def create_grid(locked_positions={}):
        grid = [[(0,0,0) for x in range(10)] for x in range(20)]
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (j,i) in locked_positions:
                    c = locked_positions[(j,i)]
                    grid[i][j] = c
        return grid
    def convert_shape_format(shape):
        positions = []
        format = shape.shape[shape.rotation % len(shape.shape)]
        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((shape.x + j, shape.y + i))
        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4) 
        return positions

    def valid_space(shape, grid):
        accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
        accepted_positions = [j for sub in accepted_positions for j in sub]
        formatted = convert_shape_format(shape)
        for pos in formatted:
            if pos not in accepted_positions:
                if pos[1] > -1:
                    return False 
        return True
    
    def check_lost(positions):
        for pos in positions:
            x, y = pos
            if y < 1:
                return True
        return False

    def get_shape():
        global shapes, shape_colors
        shapes = [S, Z, I, O, J, L, T]
        return Piece(5, 0, random.choice(shapes))

    def draw_text_middle(text, size, color, surface):
        font = pygame.font.SysFont('comicsans', size, bold=True)
        label = font.render(text, 1, color)
        surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2), top_left_y + play_height/2 - label.get_height()/2))

    def draw_grid(surface, row, col):
        sx = top_left_x
        sy = top_left_y
        for i in range(row):
            pygame.draw.line(surface, (128,128,128), (sx, sy+ i*30), (sx + play_width, sy + i * 30))
            for j in range(col):
                pygame.draw.line(surface, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + play_height))

    def clear_rows(grid, locked):
        inc = 0
        for i in range(len(grid)-1,-1,-1):
            row = grid[i]
            if (0, 0, 0) not in row:
                inc += 1
                ind = i
                for j in range(len(row)):
                    try:
                        del locked[(j, i)] 
                    except:
                        continue
        if inc > 0:
            for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < ind:
                    newKey = (x, y + inc)
                    locked[newKey] = locked.pop(key)

    def draw_next_shape(shape, surface):
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Upcoming Block', 1, (0,0,0))
        sx = top_left_x + play_width + 50
        sy = top_left_y + play_height/2 - 100
        format = shape.shape[shape.rotation % len(shape.shape)]
        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, shape.color, (sx + j*30, sy + i*30, 30, 30), 0)
        surface.blit(label, (sx + 10, sy- 30))

    def draw_window(surface):
        surface.fill((255,255,255))
        font = pygame.font.SysFont('comicsans', 60)
        label = font.render('BLOCK GAME', 1, (0,0,0))
        surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(surface, grid[i][j], (top_left_x + j* 30, top_left_y + i * 30, 30, 30), 0)
        draw_grid(surface, 20, 10)
        pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

    def main():
        global grid
        locked_positions = {}
        grid = create_grid(locked_positions)
        change_piece = False
        run = True
        current_piece = get_shape()
        next_piece = get_shape()
        clock = pygame.time.Clock()
        fall_time = 0
        while run:
            fall_speed = 0.27
            grid = create_grid(locked_positions)
            fall_time += clock.get_rawtime()
            clock.tick()
            if fall_time/1000 >= fall_speed:
                fall_time = 0
                current_piece.y += 1
                if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                    current_piece.y -= 1
                    change_piece = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        current_piece.x -= 1
                        if not valid_space(current_piece, grid):
                            current_piece.x += 1
                    elif event.key == pygame.K_RIGHT:
                        current_piece.x += 1
                        if not valid_space(current_piece, grid):
                            current_piece.x -= 1
                    elif event.key == pygame.K_UP:
                        current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                        if not valid_space(current_piece, grid):
                            current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
                    if event.key == pygame.K_DOWN:
                        current_piece.y += 1
                        if not valid_space(current_piece, grid):
                            current_piece.y -= 1
            shape_pos = convert_shape_format(current_piece)
            for i in range(len(shape_pos)):
                x, y = shape_pos[i]
                if y > -1:
                    grid[y][x] = current_piece.color
            if change_piece:
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    locked_positions[p] = current_piece.color
                current_piece = next_piece
                next_piece = get_shape()
                change_piece = False
                clear_rows(grid, locked_positions)
    
            draw_window(win)
            draw_next_shape(next_piece, win)
            pygame.display.update()
            if check_lost(locked_positions):
                run = False
        draw_text_middle("Game Over", 40, (255,0,0), win)
        pygame.display.update()
        pygame.time.delay(2000)
    win = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption('Block game made by Varun Sharma')
    main()
def Snake_Game():
    pygame.init()
    class cube (object):
        rows=20
        w=500
        def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
            self.pos=start
            self.dirnx=1
            self.dirny=0
            self.color=color
        def move(self, dirnx, dirny):
            self.dirnx=dirnx
            self.dirny=dirny
            self.pos=(self.pos[0]+self.dirnx, self.pos[1]+self.dirny)
        def draw(self, surface, eyes=False):
            dis = self.w // self.rows
            i = self.pos[0]
            j = self.pos[1]
    
            pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
            if eyes:
                centre = dis//2
                radius = 3
                circleMiddle = (i*dis+centre-radius,j*dis+8)
                circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
                pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
                pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)


    class snake(object):
        body=[]
        turns={}
        def __init__(self, color, pos):
            self.color=color
            self.head=cube(pos)
            self.body.append(self.head)
            self.dirnx=0
            self.dirny=1
        def move(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                keys=pygame.key.get_pressed()
                for key in keys:
                    if keys[pygame.K_LEFT]:
                        self.dirnx = -1
                        self.dirny = 0
                        self.turns[self.head.pos[:]]=[self.dirnx, self.dirny]
                    elif keys[pygame.K_RIGHT]:
                        self.dirnx = 1
                        self.dirny = 0
                        self.turns[self.head.pos[:]]=[self.dirnx, self.dirny]
                    elif keys[pygame.K_UP]:
                        self.dirnx = 0
                        self.dirny = -1
                        self.turns[self.head.pos[:]]=[self.dirnx, self.dirny]
                    elif keys[pygame.K_DOWN]:
                        self.dirnx = 0
                        self.dirny = 1
                        self.turns[self.head.pos[:]]=[self.dirnx, self.dirny]
            for i, c in enumerate(self.body):
                p=c.pos[:]
                if p in self.turns:
                    turn=self.turns[p]
                    c.move(turn[0],turn[1])
                    if i == len(self.body)-1:
                        self.turns.pop(p)
                else:
                    if c.dirnx == -1 and c.pos[0]<=0:
                        c.pos=(c.rows-1, c.pos[1])
                    elif c.dirnx == 1 and c.pos[0]>=c.rows-1:
                        c.pos=(0, c.pos[1])
                    elif c.dirny == 1 and c.pos[1]>=c.rows-1:
                        c.pos=(c.pos[0],0)
                    elif c.dirny == -1 and c.pos[1]<=0:
                        c.pos=(c.pos[0],c.rows-1)
                    else:
                        c.move(c.dirnx, c.dirny)
        def reset(self, pos):
            self.head = cube(pos)
            self.body = []
            self.body.append(self.head)
            self.turns = {}
            self.dirnx = 0
            self.dirny = 1
        def addcube(self):
            tail=self.body[-1]
            dx, dy=tail.dirnx, tail.dirny
            if dx == 1 and dy == 0:
                self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
            elif dx == -1 and dy == 0:
                self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
            elif dx == 0 and dy == 1:
                self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
            elif dx == 0 and dy == -1:
                self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
            self.body[-1].dirnx = dx
            self.body[-1].dirny = dy
        def draw(self, surface):
            for i, c in enumerate(self.body):
                if i == 0:
                    c.draw(surface, True)
                else:
                    c.draw(surface)
    def drawgrid(w, rows, surface):
        sizebtwn=w//rows

        x=0
        y=0
        for l in range(rows):
            x = x + sizebtwn
            y = y + sizebtwn
            pygame.draw.line(surface, (255,255,255), (x,0), (x,w))
            pygame.draw.line(surface, (255,255,255), (0,y), (w,y))

    def redrawwindow(surface):
        global rows, width , s, snack
        surface.fill((0,0,0))
        s.draw(surface)
        snack.draw(surface)
        drawgrid(width, rows, surface)
        pygame.display.update()
    def randomsnack(rows, item):
        positions=item.body
        while True:
            x=random.randrange(rows)
            y=random.randrange(rows)
            if len(list(filter(lambda z:z.pos == (x,y), positions)))>0:
                continue
            else:
                break
        return (x,y)
    def message_box(subject, content):
        root = tk.Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        messagebox.showinfo(subject, content)
        try:
            root.destroy()
        except:
            pass
    def main():
        global width, rows, s, snack
        width=500
        heigth=500
        rows=20
        win = pygame.display.set_mode((width, heigth))
        s=snake((255,0,0),(10,10))
        snack=cube(randomsnack(rows, s), color=(0,255,0))
        flage=True
        
        clock=pygame.time.Clock()
        
        while flage:
            pygame.time.delay(50)
            clock.tick(10)
            s.move()
            if s.body[0].pos == snack.pos:
                s.addcube()
                snack=cube(randomsnack(rows, s), color=(0,255,0))
            for x in range(len(s.body)):
                if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                    print('Score: ', len(s.body))
                    message_box("Game over", f"Your score: {len(s.body)}")
                    s.reset((10,10))
                    break
            redrawwindow(win)


    main()
def Ping_game():
    pygame.init()
    win=pygame.display.set_mode((750,500))
    pygame.display.set_caption("Pong Game made by varun sharma")
    gra=(185,185,185)
    bl=(0,0,0)
    blu=(0,0,255)
    gr=(0,255,0)
    yl=(255,255,0)
    red=(255,0,0)
    run=True
    class Paddle1(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface([10, 75])
            self.image.fill(gra)
            self.rect = self.image.get_rect()
            self.points = 0
    class Paddle2(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface([10, 75])
            self.image.fill(red)
            self.rect = self.image.get_rect()
            self.points = 0
    class Ball(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface([10, 10])
            self.image.fill(blu)
            self.rect = self.image.get_rect()
            self.speed = 10
            self.dx = 1
            self.dy = 1
    paddle1 = Paddle1()
    paddle1.rect.x = 25
    paddle1.rect.y = 225
    paddle2 = Paddle2()
    paddle2.rect.x = 715
    paddle2.rect.y = 225
    paddle_speed = 15
    pong = Ball()
    pong.rect.x = 375
    pong.rect.y = 250
    all_sprites = pygame.sprite.Group()
    all_sprites.add(paddle1, paddle2, pong)
    def redraw():
        win.fill(bl)
        font = pygame.font.SysFont('Comic Sans MS', 30)
        text = font.render('PONG', False, yl)
        textRect = text.get_rect()
        textRect.center = (750 // 2, 25)
        win.blit(text, textRect)
        p1_score = font.render(str(paddle1.points), False, gr)
        p1Rect = p1_score.get_rect()
        p1Rect.center = (50, 50)
        win.blit(p1_score, p1Rect)
        p2_score = font.render(str(paddle2.points), False, gr)
        p2Rect = p2_score.get_rect()
        p2Rect.center = (700, 50)
        win.blit(p2_score, p2Rect)
        all_sprites.draw(win)
        pygame.display.update()
    def message_box(subject, content):
        root = tk.Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        messagebox.showinfo(subject, content)
        try:
            root.destroy()
        except:
            pass
    def main():
        run=True
        while run:
            pygame.time.delay(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            key = pygame.key.get_pressed()
            if key[pygame.K_w]:
                paddle1.rect.y += -paddle_speed
            if key[pygame.K_s]:
                paddle1.rect.y += paddle_speed
            if key[pygame.K_UP]:
                paddle2.rect.y += -paddle_speed
            if key[pygame.K_DOWN]:
                paddle2.rect.y += paddle_speed
            pong.rect.x += pong.speed * pong.dx
            pong.rect.y += pong.speed * pong.dy
            if pong.rect.y > 490:
                pong.dy = -1
            if pong.rect.y < 1:
                pong.dy = 1
            if pong.rect.x > 740:
                pong.rect.x, pong.rect.y = 375, 250
                pong.dx = -1
                paddle1.points += 1
            if pong.rect.x < 1:
                pong.rect.x, pong.rect.y = 375, 250
                pong.dx = 1
                paddle2.points += 1
            if paddle1.rect.colliderect(pong.rect):
                pong.dx = 1
            if paddle2.rect.colliderect(pong.rect):
                pong.dx = -1
            redraw()
            if paddle1.points==5:
                message_box("Game over", "palyer 1 win")
                paddle1.points=0
                paddle2.points=0
                continue
            elif paddle2.points==5:
                message_box("Game over", "palyer 2 win")
                paddle1.points=0
                paddle2.points=0
                continue
    main()
run=True
BG=button((0,255,0),15,50,250,100,"Play Block Game")
SG=button((0,255,0),15,200,250,100,"Play Snake Game")
PG=button((0,255,0),15,350,250,100,"Play Ping")
while run:
    redrawwindow()
    pygame.display.update()
    for event in pygame.event.get():
        pos=pygame.mouse.get_pos()
        if event.type==pygame.QUIT:
            run=False
            pygame.quit
            quit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            if BG.isOver(pos):
                Block_Game()
            if SG.isOver(pos):
                Snake_Game()
            if PG.isOver(pos):
                Ping_game()
        if event.type==pygame.MOUSEMOTION:
            if SG.isOver(pos):
                SG.color=(255,0,0)
            else:
                SG.color=(0,255,0)
            if BG.isOver(pos):
                BG.color=(255,0,0)
            else:
                BG.color=(0,255,0)
            if PG.isOver(pos):
                PG.color=(255,0,0)
            else:
                PG.color=(0,255,0)