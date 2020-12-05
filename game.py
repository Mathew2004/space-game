import pygame
from pygame import mixer
import random
import math

pygame.init()
#create screen
screen = pygame.display.set_mode((800,600))

#game title
pygame.display.set_caption("Space Invaders")

#set logo
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

#background image
background = pygame.image.load('background.jpg')

#Background Sound
mixer.music.load('bg.mp3')
mixer.music.play(-1)

#Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(50)

#Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 2
bullet_state = "ready"

#Diplay Score
score_value = 0

font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

#Level
level_font = pygame.font.Font("freesansbold.ttf", 32)
level_value = 1
def level():
    level = level_font.render("Level: "+ str(level_value),True, (255,255,255))
    screen.blit(level, (400, 10))

#gameover
gameover_font = pygame.font.Font("freesansbold.ttf", 72)
def game_over_text():
    gameover = gameover_font.render("GAME OVER",True, (255,255,255))
    screen.blit(gameover, (200, 250))

def score(x,y):
    score = font.render("Score: "+ str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

#player function
def player(x,y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16 , y+10))

#killEnemy
def isColision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX,2) + math.pow(enemyY-bulletY,2)) 

    if distance < 27:
        return True
    else:
        return False

#Game Loop
running = True
while running:
    for event in pygame.event.get():
        #Exit when click on exit
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
         

    #Add background color of screen
    screen.fill((0,0,0))
    #BackgroundImg
    screen.blit(background,(0,0))

    #Checking bundaries of spaceship and enemy
    playerX += playerX_change
    #Add player Movement
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #Add Enemy Movement
    for i in range(num_of_enemies):
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break


        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1

            enemyY[i] += enemyY_change[i]

         #Colision
        colision = isColision(enemyX[i], enemyY[i], bulletX, bulletY)
        if colision:
            colisionSound = mixer.Sound('explosion.wav')
            colisionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyImg[i] = pygame.image.load("enemy.png")
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
            if score_value == 10:
                level_value = 2
                bulletY_change = 2
                num_of_enemies = 5
                background = pygame.image.load('level2.jpg')
                
            if score_value == 25:
                level_value = 3
                bulletY_change = 2
                num_of_enemies = 4
                background = pygame.image.load('level3.jpg')
            if score_value == 40:
                level_value = 4
                bulletY_change = 2
                num_of_enemies = 6
                background = pygame.image.load('level4.jpg')
            if score_value == 55:
                level_value = 5
                bulletY_change = 2
                num_of_enemies = 6
                background = pygame.image.load('level5.jpg')

        enemy(enemyX[i], enemyY[i], i)
   
    #Bullet Movement 
    #Multiple bullet
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

   

    player(playerX,playerY)
    score(textX,textY)
    level()
    pygame.display.update()
