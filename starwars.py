import pygame
import random
import math
from pygame import mixer

# initializing pygame
pygame.init()
screen=pygame.display.set_mode((800,600))

pygame.display.set_caption('Star Wars Old School')

icon=pygame.image.load("requirements\\icon(1).png")
pygame.display.set_icon(icon)
bg=pygame.image.load("images\\background.jpg")

# caption and icon
pygame.display.set_caption("Welcome to Space Invaders Game by:- styles")

#bullet
bulletImage = pygame.image.load('images\\bullet.png')
bullet_X = 0
bullet_Y = 500
bullet_Xchange = 0
bullet_Ychange = 4
bullet_state = False
#spaceship
spaceship = pygame.image.load('images\\spaceship.png')
spaceship_X = 370
spaceship_Y = 523
spaceship_Xchange = 0
# Aliens
aliensImage = []
aliens_X = []
aliens_Y = []
aliens_Xchange = []
aliens_Ychange = []
no_of_aliens = 40
# Score
score_val = 0
scoreX = 5
scoreY = 5
font = pygame.font.Font('freesansbold.ttf', 20)

# Game Over display
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Points: " + str(score_val), True, (255,255,255))
    screen.blit(score, (x , y ))

def game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(game_over_text, (190, 250))

# Background Sound
mixer.music.load('sounds\\background.mp3')
mixer.music.play(-1)

for num in range(no_of_aliens):
    aliensImage.append(pygame.image.load('images\\aliens.png'))
    aliens_X.append(random.randint(64, 737))
    aliens_Y.append(random.randint(30, 180))
    aliens_Xchange.append(1.2)
    aliens_Ychange.append(50)

def disp_spaceship(x, y):
    screen.blit(spaceship, (x , y))

def disp_alien(x, y, i):
    screen.blit(aliensImage[i], (x, y))

def bullet(x, y):
    global bullet_state
    screen.blit(bulletImage, (x, y))
    bullet_state = True

#Logic behind collision of bullet with the aliens
def isCollision(x1, x2, y1, y2):
    distance = math.sqrt((math.pow(x1 - x2,2)) + (math.pow(y1 - y2,2)))
    if distance <= 50:
        return True
    else:
        return False

# Game Loop
running = True
while running:

    screen.blit(bg,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #Arrow keys to control player's movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                spaceship_Xchange = -4
            if event.key == pygame.K_RIGHT:
                spaceship_Xchange = 4
            if event.key == pygame.K_SPACE: #spacebar key to fire bullet
                # Bullet Fire
                if bullet_state ==False:
                    bullet_X = spaceship_X
                    bullet(bullet_X, bullet_Y)
                    bullet_sound = mixer.Sound('sounds\\bullet.mp3')
                    bullet_sound.play()
        #constricting movement of spaceship along y
        if event.type == pygame.KEYUP:
            spaceship_Xchange = 0

    # Change in position of spaceship along x-direction
    spaceship_X += spaceship_Xchange
    for i in range(no_of_aliens):
        aliens_X[i] += aliens_Xchange[i]

    # Logic behind bullet movement
    if bullet_Y <= 0:
        bullet_Y = 600
        bullet_state = False
    if bullet_state ==True:
        bullet(bullet_X, bullet_Y)
        bullet_Y -= bullet_Ychange
 
 #Checking for game over ,i.e, when any aliens strikes the spaceship
    for i in range(no_of_aliens):
        if no_of_aliens==0:
            game_over_text = game_over_font.render("Victory", True, (255,255,255))
            screen.blit(game_over_text, (190, 250))
        if aliens_Y[i] >= 450:
            if abs(spaceship_X-aliens_X[i]) < 80:
                for j in range(no_of_aliens):
                    aliens_Y[j] = 2000
                    explosion_sound = mixer.Sound('sounds\\explosion.wav')
                    explosion_sound.play()
                game_over()
                break
 
        if aliens_X[i] >= 735 or aliens_X[i] <= 0:
            aliens_Xchange[i] *= -1
            aliens_Y[i] += aliens_Ychange[i]
        # Collision
        collision = isCollision(bullet_X, aliens_X[i], bullet_Y, aliens_Y[i])
        if collision:
            score_val += 1
            bullet_Y = 600
            bullet_state = False
            aliens_X[i] = random.randint(64, 736)
            aliens_Y[i] = random.randint(30, 200)
            aliens_Xchange[i] *= -1
            no_of_aliens-=1
            
        disp_alien(aliens_X[i], aliens_Y[i], i)

    # restricting the spaceship from going out of game screen
    if spaceship_X <= 16:
        spaceship_X = 16;
    elif spaceship_X >= 750:
        spaceship_X = 750

    disp_spaceship(spaceship_X, spaceship_Y)
    show_score(scoreX, scoreY)
    pygame.display.update()

