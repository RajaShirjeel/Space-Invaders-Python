import pygame
import sys
import random
from math import sqrt, pow
from pygame import *
from pygame import mixer



pygame.init()
mixer.init()  
clock = pygame.time.Clock()
width = 1000
height = 800
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Space Invaders")
backgroundImg = pygame.image.load("imp_resources/images/background.png")
backgroundImg = pygame.transform.scale(backgroundImg, (width, height))
font = pygame.font.SysFont('arial', 36)
mixer.music.load("imp_resources/sounds/feed-the-machine-classic-arcade-game-116846.mp3")
mixer.music.play(-1)

# player 
playerImg = pygame.image.load("imp_resources/images/player.png")
playerImg = pygame.transform.scale(playerImg, (60, 60))
playerX = 450
playerY = 700
playerX_change = 0
playerY_change = 0

# enemies
gap_between_enemies = 100
number_of_enemies = 6
enemiesImg = []
enemiesX = []
enemiesY = [] * number_of_enemies
enemiesX_change = []
enemiesY_change = []


for i in range(number_of_enemies):
    original_enemy_image = pygame.image.load("imp_resources/images/ufo.png")
    scaled_enemy_image =  pygame.transform.scale(original_enemy_image, (50, 50))
    enemiesImg.append(scaled_enemy_image)
    enemiesX.append(random.randint(0, 300))
    enemiesY.append(random.randint(0, 150))
    enemiesX_change.append(0)
    enemiesY_change.append(0.5)
    if i > 0:
        enemiesX[i] = enemiesX[i - 1] + gap_between_enemies
    

# bullet
bulletImg = pygame.image.load("imp_resources/images/bullet2.png")
bulletImg = pygame.transform.scale(bulletImg, (50, 50))
bulletX = 450
bulletY = 700
bulletX_change = 0
bulletY_change = 10
bullet_state = 'ready'

# score
player_score = 0

def display_score():
    score_text = font.render("Score: " + str(player_score), True, (255, 255, 255))
    screen.blit(score_text, (0, 0))

def game_over():
    score_text = font.render("Game Over", True, (255, 255, 255))
    screen.blit(score_text, (400, 400))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x+16, y+10))
    
def detect_collision(bullet_x, bullet_y, enemy_x, enemy_y):
    # let's detect the collision using multiple points along the bullet path
    for offset in range(5, 26, 5):  # check points every 5 pixels
        check_x = bullet_x + offset
        check_y = bullet_y
        distance = sqrt(pow(enemy_x - check_x, 2) + pow(enemy_y - check_y, 2))
        if distance < 25:
            return True
    return False
        
def enemy(x, y, i):
    screen.blit(enemiesImg[i], (x, y))


def check_game_over():
    for i in range(len(enemiesX)):
        if enemiesY[i] > 760:
            game_over()
            return True
    return False
    
running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                playerX_change = -5

            if event.key == K_RIGHT:
                playerX_change = 5
        if event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                playerX_change = 0

        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if bullet_state == "ready":
                bulletX = playerX 
                bulletSound = mixer.Sound("imp_resources/sounds/shoot.wav")
                bulletSound.play()
                fire_bullet(bulletX, bulletY)

    for i in range(number_of_enemies):
        enemiesX [i] += enemiesX_change[i]
        enemiesY[i] += enemiesY_change[i]


    # stop the player from going beyond the walls   
    if playerX >= 935:
        playerX = 935
    
    if playerX <= 0:
        playerX = 0

    playerX += playerX_change

    screen.blit(backgroundImg, (0, 0))
    screen.blit(playerImg, (playerX, playerY))

    for i in range(number_of_enemies):
        enemy(enemiesX[i], enemiesY[i], i)
        if check_game_over():
            break
            


    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
        bulletY = playerY

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # detect collisions
    for i in range(len(enemiesX)):
        if detect_collision(bullet_x=bulletX, bullet_y=bulletY, enemy_x=enemiesX[i], enemy_y=enemiesY[i]):
            explosionSound = mixer.Sound("imp_resources/sounds/invaderkilled.wav")
            explosionSound.play()
            enemiesX[i] = 2000000000
            enemiesY[i] = -2000000000
            player_score += 10
            enemiesX.append(random.randint(100, 600))
            enemiesY.append(-50)
            original_enemy_image = pygame.image.load("imp_resources/images/ufo.png")
            scaled_enemy_image = pygame.transform.scale(original_enemy_image, (50, 50))
            enemiesImg.append(scaled_enemy_image)
            enemiesX_change.append(0)
            enemiesY_change.append(1)
        enemiesY[i] += enemiesY_change[i]
        
        enemy(enemiesX[i], enemiesY[i], i)

                    
            
    display_score()


    pygame.display.flip()
    clock.tick(30) 