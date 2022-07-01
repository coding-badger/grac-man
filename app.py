import sys, os
import pygame
from random import randrange


W, H = 896, 992
WIDTH, HEIGHT = 1000, 1000
ROWS = 31 #up&down
COLS = 28 #right&left
WIN = pygame.display.set_mode((W, H))
FPS = 10

BLACK = (0,0,0)
WHITE = (255,255,255)
LTGREY = (150,150,150)
GREY = (50,50,50)
YELLOW = (255,255,0)
PURPLE = (255,0,255)

squares = []
img_coin = pygame.transform.smoothscale(pygame.image.load(os.path.join('assets','coin.png')), ((WIDTH/ROWS)-22,(WIDTH/ROWS)-22))
img_gracman1 = pygame.transform.smoothscale(pygame.image.load(os.path.join('assets','gracman1.png')), ((WIDTH/ROWS),(WIDTH/ROWS)))
img_gracman2 = pygame.transform.smoothscale(pygame.image.load(os.path.join('assets','gracman2.png')), ((WIDTH/ROWS),(WIDTH/ROWS)))
img_bg = pygame.image.load(os.path.join('assets','background.png'))



class Game(object):
    pygame.display.set_caption('Grac-Man by Jared')
    clock = pygame.time.Clock()
    
    def __init__(self, surface=WIN, score=0):
        self.surface = surface

        self.level = Level(self.surface)
        #self.level.generate()
        self.player = Player(self.surface)
        self.ghosts = Ghost(self.surface,)
        self.squares = Squares(self.surface)
        
        self.score = score

    
    def drawGrid(self):  
        sizeBtwn = HEIGHT // ROWS

        x = 0
        y = 0
        for l in range(COLS):
            x = x + sizeBtwn
            pygame.draw.line(self.surface, LTGREY, (x,0), (x,HEIGHT)) #draw vertical lines
        for l in range(ROWS):
            y = y + sizeBtwn
            pygame.draw.line(self.surface, LTGREY, (0,y), (WIDTH,y)) #draw horizontal lines        

    def background(self):
        WIN.blit(self.level.bg, (0,0))
 
    def update(self):
        pygame.time.delay(10)
        self.clock.tick(FPS)
        self.player.move()
        self.ghosts.move()
        self.background()
        #self.drawGrid()
        self.squares.draw()
        self.level.draw()
        self.player.draw()
        #self.ghosts.draw()

        pygame.display.update()    


class Level(object):

    def __init__(self, surface=WIN, level=1):
        self.level = level
        self.surface = surface
        self.bg = img_bg

        self.gridmap = []
        self.gridmap_temp = []

        with open('gridmap1.txt', 'r') as f:
            next(f)
            contents = f.read()
            lines = contents.split('\n')
            for line in lines:
                self.gridmap.append([int(e) for e in line.split(',')])
                self.gridmap_temp.append([int(e) for e in line.split(',')])
        f.close()

    def generate(self):
        for i in range(len(self.gridmap)):
            for j in range(len(self.gridmap[i])):
                if self.gridmap[i][j] != 0:
                    self.gridmap[i][j] = 2                    

    def draw(self):
        dis = WIDTH // ROWS
        for i in range(len(self.gridmap)):
            for j in range(len(self.gridmap[i])):
                if self.gridmap[i][j] == 2:
                    #pygame.draw.rect(self.surface, WHITE, (i*dis+9, j*dis+9, dis-18, dis-18))
                    WIN.blit(img_coin, (i*dis+11, j*dis+11, dis-22, dis-22))
        

class Squares(object):

    def __init__(self, surface, color=GREY):
        self.surface = surface
        self.color = color
        self.squares = []

    def draw(self):
        dis = WIDTH//ROWS
        if any(pygame.mouse.get_pressed()):
                x, y = pygame.mouse.get_pos() 
                w_x, w_y = x // (HEIGHT//ROWS), y // (HEIGHT//ROWS)
                print(f'{w_x},{w_y}')
                print(f'Val at in gridmap: {game.level.gridmap[w_x][w_y]}')
                print(f'Player Pos: {game.player.pos}')
                if (w_x,w_y) not in self.squares:
                    self.squares.append((w_x,w_y))
        for l, c in enumerate(self.squares):
             pygame.draw.rect(self.surface, LTGREY, (self.squares[l][0]*dis+1, self.squares[l][1]*dis+1, dis-1, dis-1))


class Player(object):

    def __init__(self, surface, moving=True, start=(13,17), dirnx=0, dirny=0, color=YELLOW):
        self.surface = surface
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color
        self.moving = moving
        self.img_count = 0
        self.left = False
        self.right = True
        self.up = False
        self.down = False

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Goodbye!\n')
                #save_layout(1)

                pygame.quit()
                sys.exit(0)

            keys = pygame.key.get_pressed()

            for key in keys:                        
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.left = True
                    self.right = False
                    self.up = False
                    self.down = False

                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.left = False
                    self.right = True
                    self.up = False
                    self.down = False

                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.left = False
                    self.right = False
                    self.up = True
                    self.down = False

                if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.left = False
                    self.right = False
                    self.up = False
                    self.down = True

        if self.dirnx == -1 and self.pos[0] <= 0: self.pos = (COLS, self.pos[1])        #if traveling left      and reach left edge,        move cube to right edge
        elif self.dirnx == 1 and self.pos[0] >= COLS-1: self.pos = (-1, self.pos[1])    #if traveling right     and reach right edge,       move cube to left edge
        elif self.dirny == 1 and self.pos[1] >= ROWS-1: self.pos = (self.pos[0], -1)    #if traveling down      and reach bottom edge,      move cube to top edge
        elif self.dirny == -1 and self.pos[1] <= 0: self.pos = (self.pos[0], ROWS)      #if traveling up        and reach top edge          move cube to bottom edge

        i = game.player.pos
        try:
        ###walls left###      
            if game.level.gridmap[(i[0])-1][i[1]] == 0 and game.player.dirnx == -1:
                game.player.moving = False
            if game.level.gridmap[(i[0])-1][i[1]] != 0 and game.player.dirnx == -1:
                game.player.moving = True
        ###walls right###
            if game.level.gridmap[(i[0])+1][i[1]] == 0 and game.player.dirnx == 1:
                game.player.moving = False
            if game.level.gridmap[(i[0])+1][i[1]] != 0 and game.player.dirnx == 1:
                game.player.moving = True
        ###walls up###
            if game.level.gridmap[i[0]][(i[1])-1] == 0 and game.player.dirny == -1:
                game.player.moving = False
            if game.level.gridmap[i[0]][(i[1])-1] != 0 and game.player.dirny == -1:
                game.player.moving = True
        ###walls down###
            if game.level.gridmap[i[0]][(i[1])+1] == 0 and game.player.dirny == 1:
                game.player.moving = False
            if game.level.gridmap[i[0]][(i[1])+1] != 0 and game.player.dirny == 1:
                game.player.moving = True
        except:pass
        ###coins###
        try:
            if game.level.gridmap[i[0]][i[1]] == 2:
                game.level.gridmap[i[0]][i[1]] = 1
                game.score = game.score + 10
                print(f'Score: {game.score}')
        except:pass

        if self.moving == True:
            self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny) # add new position to existing position in order to move

    def draw(self):
        if self.img_count == 4:
            self.img_count = 0

        dis = WIDTH // ROWS #size of square
        i = self.pos[0]
        j = self.pos[1]

        if self.right:
            if self.img_count == 0 or self.img_count == 1:
                WIN.blit(img_gracman1, (i*dis+1, j*dis+1, dis-1, dis-1))
            elif self.img_count == 2 or self.img_count == 3:
                WIN.blit(img_gracman2, (i*dis+1, j*dis+1, dis-1, dis-1))
        if self.left:
            rot1 = pygame.transform.rotate(img_gracman1, 180)
            rot2 = pygame.transform.rotate(img_gracman2, 180)
            if self.img_count == 0 or self.img_count == 1:
                WIN.blit(rot1, (i*dis+1, j*dis+1, dis-1, dis-1))
            elif self.img_count == 2 or self.img_count == 3:
                WIN.blit(rot2, (i*dis+1, j*dis+1, dis-1, dis-1))
        if self.up:
            rot1 = pygame.transform.rotate(img_gracman1, 90)
            rot2 = pygame.transform.rotate(img_gracman2, 90)
            if self.img_count == 0 or self.img_count == 1:
                WIN.blit(rot1, (i*dis+1, j*dis+1, dis-1, dis-1))
            elif self.img_count == 2 or self.img_count == 3:
                WIN.blit(rot2, (i*dis+1, j*dis+1, dis-1, dis-1))
        if self.down:
            rot1 = pygame.transform.rotate(img_gracman1, 270)
            rot2 = pygame.transform.rotate(img_gracman2, 270)
            if self.img_count == 0 or self.img_count == 1:
                WIN.blit(rot1, (i*dis+1, j*dis+1, dis-1, dis-1))
            elif self.img_count == 2 or self.img_count == 3:
                WIN.blit(rot2, (i*dis+1, j*dis+1, dis-1, dis-1))                                                


        self.img_count = self.img_count + 1


class Ghost(object):

    def __init__(self, surface, dirnx=0, dirny=0, color=PURPLE):
        self.surface = surface
        self.pos = (randrange(40), randrange(40))
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color
        self.count = 0
        self.i = 0

    def move(self):
        if self.count >= 4:
            self.i = randrange(4)

        if self.i == 0:#left
            self.dirnx = -1
            self.dirny = 0
        elif self.i == 1:#right
            self.dirnx = 1
            self.dirny = 0
        elif self.i == 2:#up
            self.dirnx = 0
            self.dirny = -1
        elif self.i == 3:#down
            self.dirnx = 0
            self.dirny = 1

        if self.dirnx == -1 and self.pos[0] <= 0: self.pos = (ROWS, self.pos[1])
        elif self.dirnx == 1 and self.pos[0] >= ROWS-1: self.pos = (-1, self.pos[1])
        elif self.dirny == 1 and self.pos[1] >= ROWS-1: self.pos = (self.pos[0], -1)
        elif self.dirny == -1 and self.pos[1] <= 0: self.pos = (self.pos[0], ROWS)

        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
        self.count = self.count + 1
    
    def draw(self,):
            dis = WIDTH // ROWS
            i = self.pos[0]
            j = self.pos[1]
            
            pygame.draw.rect(self.surface, self.color, (i*dis+1, j*dis+1, dis-1, dis-1))


def save_layout(val): #saves changes to gridmap based on selected squares to specified value to TEMP file
    game.squares.squares.sort()
    cnt = 0
    for x in range(len(game.squares.squares)):
        i = game.squares.squares[cnt][0]
        j = game.squares.squares[cnt][1]

        game.level.gridmap_temp[i][j] = val
        cnt += 1
    
    try:
        with open('gridmap1temp.txt', 'w') as f:
            for i in range(COLS):
                f.write('\n')
                for j in range(ROWS):
                    f.write(str(game.level.gridmap_temp[i][j])) # SAVED GRIDMAP FILES ARE ROTATED 90 degrees
                    if j != ROWS-1:
                        f.write(",")
        f.close()
    except:print(f'{j} {i}')




def main():
    global game

    pygame.init
    running = True
    game = Game()

    while running:

        game.update()

if __name__ == "__main__":
    main()

#fix movement so player doesn't stop moving forward when changing direction directly into wall