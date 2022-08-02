import math
import pygame
import random

# initialize pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600)) # height = 600, width = 800

# background
background = pygame.image.load('./assets/img/background.jpg')

# caption and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('./assets/img/ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('./assets/img/spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0 # the variable for moving

def player(x, y):
    screen.blit(playerImg, (x, y))

# -----End of player attributes-----    

# Enemy
img_of_enemy = ['./assets/img/ufo-enemy.png', './assets/img/space-ship.png', './assets/img/alien.png']
enemyImg = list()
enemyX = list()
enemyY = list()
enemyX_change = list()
enemyY_change = list()
nums_of_enemy = 15

for i in range(nums_of_enemy):
    enemyImg.append(pygame.image.load(random.choice(img_of_enemy)))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(20,30))
    enemyX_change.append(0.2) # the variable for moving
    enemyY_change.append(30)

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# -----End of enemy attributes-----
    
# Bullet
# Ready - you can not see the bullet on the screen
# Fire - the bullet is currently moving
bulletImg = pygame.image.load('./assets/img/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0 # the variable for moving
bulletY_change = 0.8
bullet_state = 'ready'

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 20, y + 11))

# -----End of bullet attributes----- 

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Collision
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# initial important variables
running = True

# main execute loop
while running:
    # screen color
    # screen.fill((0, 150, 0))
    
    # background image
    screen.blit(background, (0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
               playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
               playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    # get the current x coordinate
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)               
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    
    playerX += playerX_change
    
    # to avoid the spaceship go beyond the screen
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
        
    
    # to avoid the enemy go beyond the screen
    for i in range(nums_of_enemy):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]
        
        # collisions
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(20, 30)
        
        enemy(enemyX[i], enemyY[i], i)
             
    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
        

    player(playerX, playerY)
    show_score(textX, textY)
    
    # to display the changes of the game
    pygame.display.flip()
    
pygame.quit() #delete all the memory of the program when exit