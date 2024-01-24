import pygame
from random import randint
from random import choice
import math

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
FPS = 60

lives = 3
running = True
ants = []
bees = []
score = 0
game_started = 0 # 0 - nije startano, 1 - startano, 2 - game over
ctr = 100
new_ants = 3
high_score = 0

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

background = pygame.image.load("images/floor.jpg")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

ant_img = pygame.image.load("images/ant.png").convert_alpha()
ant_img = pygame.transform.scale(ant_img, (70, 75))
ant_img = pygame.transform.rotate(ant_img, -135)

heart = pygame.image.load("images/heart.png").convert_alpha()
heart = pygame.transform.scale(heart, (50, 50))

heart_empty = pygame.image.load("images/heart.png").convert_alpha()
heart_empty = pygame.transform.scale(heart_empty, (50, 50))
heart_empty.set_alpha(100)

bee_img = pygame.image.load("images/bee.png").convert_alpha()
bee_img = pygame.transform.scale(bee_img, (75, 75))
bee_img = pygame.transform.rotate(bee_img, 180)

stain_img = pygame.image.load("images/stain.png").convert_alpha()

class Ant():
    def __init__(self, x, y, v_x, v_y):
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
        self.squashed = None
        self.rect = pygame.Rect(x, y, 70, 75)   

    def move(self):
        global lives

        if self.x + self.v_x + 35 <= 0 or self.x + self.v_x + 80 >= SCREEN_WIDTH:
            self.v_x *= -1

        self.x += self.v_x
        self.y += self.v_y

        self.rect = pygame.Rect(self.x + 35, self.y + 35, 70, 75) 

        if self.y >= SCREEN_HEIGHT:
            ants.remove(self)
            lives -= 1
        
        if randint(0, 100) <= 5:
            self.v_x = randint(-3, 3)
            self.v_y = randint(1, 3)

    def draw(self):
        if self.squashed is None:
            angle = math.degrees(math.atan(self.v_x / self.v_y))
            screen.blit(pygame.transform.rotate(ant_img, angle), (self.x, self.y))
            #pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        elif self.squashed < 100:
            ant_squashed = pygame.transform.scale(stain_img, (70, 70))
            ant_squashed.set_alpha((1 - self.squashed / 100) * 255)
            
            self.squashed += 1

            screen.blit(ant_squashed, (self.x + 20, self.y + 20))
        elif self in ants:
            ants.remove(self)

class Bee():
    def __init__(self, x, y, v_x, v_y):
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
        self.clicked = None
        self.rect = pygame.Rect(x, y, 75, 75)   

    def move(self):
        self.x += self.v_x
        self.y += self.v_y

        self.rect = pygame.Rect(self.x + 35, self.y + 35, 75, 75) 

        if self.x + self.v_x + 35 <= 0 or self.x + self.v_x + 80 >= SCREEN_WIDTH:
            self.v_x *= -1

        if self.y + self.v_y + 35 <= 60 or self.y + self.v_y + 80 >= SCREEN_HEIGHT:
            self.v_y *= -1 

        if self.clicked is not None:
            self.clicked += 1

        if self.clicked == 30:
            self.clicked = None

        if randint(0, 100) <= 1:
            self.v_x = randint(-2, 2)
            self.v_y = randint(-2, 2)
            while self.v_y == 0:
                self.v_y = randint(-2, 2)

    def draw(self):
        angle = math.degrees(math.atan(self.v_x / self.v_y))
        if self.v_y < 0:
            angle += 180
        if self.clicked is None or self.clicked > 10 and self.clicked < 20:    
            screen.blit(pygame.transform.rotate(bee_img, angle), (self.x, self.y))
        else:
            red_bee = bee_img.copy()
            red_bee.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
            red_bee.fill((255,0,0)[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)
            screen.blit(pygame.transform.rotate(red_bee, angle), (self.x, self.y))

def clear():
    screen.fill((255, 255, 255))

def createNewAnts(no_of_ants):
    for i in range(no_of_ants):
        x = randint(80, SCREEN_WIDTH - 220)
        y = 0
        v_x = randint(-3, 3)
        v_y = randint(1, 3)
        ants.append(Ant(x, y, v_x, v_y))

def addOneBee():
    x = randint(80, SCREEN_WIDTH - 220)
    y = 60
    v_x = randint(-2, 2)
    v_y = randint(1, 2)
    bees.append(Bee(x, y, v_x, v_y))

def drawLives():
    x = SCREEN_WIDTH - 180
    for i in range(lives):
        screen.blit(heart, (x, 5))
        x += 60
    for i in range(3 - lives):
        screen.blit(heart_empty, (x, 5))
        x += 60    

def drawScore():
    font = pygame.font.Font(None, 36)
    
    text_score = font.render("Score: " + str(score), True, (155, 155, 155))

    screen.blit(text_score, (15, 20))

def drawStartButton(down):
        if down:
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(200, 400, SCREEN_WIDTH - 400, 100), border_radius=20)
            pygame.draw.rect(screen, (165, 42, 42), pygame.Rect(210, 410, SCREEN_WIDTH - 420, 80), border_radius=20)
        else:
            pygame.draw.rect(screen, (165, 42, 42), pygame.Rect(200, 400, SCREEN_WIDTH - 400, 100), border_radius=20)

def restart():
    global lives, ants, ctr, new_ants, game_started, bees
    lives = 3
    ants = []
    bees = []
    addOneBee()
    ctr = 100
    new_ants = 3
    game_started = 1

while running:

    clock.tick(FPS)

    if ctr >= 100:
        createNewAnts(new_ants)
        ctr = 0
    else:
        ctr += 1

    clear()

    screen.blit(background, (0, 0))

    for event in pygame.event.get():
            
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for ant in ants:
                if ant.squashed is None and ant.rect.collidepoint(x, y):
                    ant.squashed = 1

                    score += 1

                    if score % 10 == 0:
                        new_ants += 1
                        addOneBee()

            for bee in bees:
                if bee.clicked is None and bee.rect.collidepoint(x, y):
                    bee.clicked = 1

                    lives -= 1
                        
        if event.type == pygame.KEYDOWN:
            if game_started != 1 and event.key == pygame.K_SPACE:
                restart()

    if game_started == 1:
        if lives == 0:
            game_started = 2

            if score > high_score:
                high_score = score

            score = 0

        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, SCREEN_WIDTH, 60))

        drawLives()

        drawScore()        

        for ant in ants:

            if ant.squashed is None:
                ant.move()
            elif ant.squashed >= 100:
                ants.remove(ant)

            ant.draw()

            
        for bee in bees:
            bee.move()

            bee.draw()
    
    elif game_started == 0:

        font = pygame.font.Font("fonts/Spirits Regular.ttf", 34)
        
        text_score = font.render("The objective of the game is to squash", True, (128, 0, 0))
        screen.blit(text_score, (SCREEN_WIDTH / 2 - text_score.get_width() / 2, 200))
        
        text_score = font.render("as many ants as you can by clicking on them.", True, (128, 0, 0))
        screen.blit(text_score, (SCREEN_WIDTH / 2 - text_score.get_width() / 2, 230))

        text_score = font.render("But, be careful, don't squash the bees,", True, (255,0,0))
        screen.blit(text_score, (SCREEN_WIDTH / 2 - text_score.get_width() / 2, 320))

        text_score = font.render("cause they will sting you!", True, (255,0,0))
        screen.blit(text_score, (SCREEN_WIDTH / 2 - text_score.get_width() / 2, 350))

        font = pygame.font.Font("fonts/A Bug s Life.ttf", 72)
        
        text_score = font.render("Press SPACE to play", True, (55, 55, 55))

        screen.blit(text_score, (SCREEN_WIDTH / 2 - text_score.get_width() / 2, SCREEN_HEIGHT - 300))

    else:

        font = pygame.font.Font("fonts/GREENFUZ.TTF", 150)
        
        text_score = font.render("GAME OVER", True, (255, 55, 55))

        screen.blit(text_score, (SCREEN_WIDTH / 2 - text_score.get_width() / 2, 100))

        font = pygame.font.Font("fonts/Official.otf", 56)
        
        text_score = font.render("HIGH SCORE: " + str(high_score), True, (55, 55, 55))

        screen.blit(text_score, (SCREEN_WIDTH / 2 - text_score.get_width() / 2, SCREEN_HEIGHT / 2 - 80))

        font = pygame.font.Font("fonts/A Bug s Life.ttf", 72)
        
        text_score = font.render("Press SPACE to restart", True, (55, 55, 55))

        screen.blit(text_score, (SCREEN_WIDTH / 2 - text_score.get_width() / 2, SCREEN_HEIGHT / 2))

    pygame.display.update()

