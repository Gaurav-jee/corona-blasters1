import pygame
import random
import math
from pygame import mixer

# initialize the game
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("corona blasters!")
icon = pygame.image.load('stop.png')
pygame.display.set_icon(icon)

# background
background = pygame.image.load("background.png")

#background sounds
mixer.music.load("background.wav")
mixer.music.play(-1)

# player
playerImg = pygame.image.load('doctor.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

enemyImg.append(pygame.image.load('enemy.png'))
enemyImg.append(pygame.image.load('bat.png'))
enemyImg.append(pygame.image.load('virus.png'))
enemyImg.append(pygame.image.load('virus (1).png'))
enemyImg.append(pygame.image.load('virus (2).png'))
enemyImg.append(pygame.image.load('virus (3).png'))

for i in range(num_of_enemies):
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(25)

# weapon
# ready = you can't see the arrow on the screen
# fire = the arrow is currently moving
arrowImg = pygame.image.load("splash.png")
arrowX = 0
arrowY = 480
arrowX_change = 0
arrowY_change = 10
arrow_state = "ready"

# score
score_value = 0
font = pygame.font.Font('font.ttf', 32)

textX = 10
textY = 10


#show score
def show_score(x, y):
    score = font.render("score : " + str(score_value), True, (66, 167, 245))
    screen.blit(score, (x, y))

#Game over
font1 = pygame.font.Font('font.ttf', 50)
def game_over_text():
    game_over = font1.render("GAME OVER !", True, (255, 0, 0))
    game_over1 = font1.render("Your Sore :" + str(score_value), True, (0, 0, 255))
    screen.blit(game_over, (300, 250))
    screen.blit(game_over1, (300, 300))

# player_function
def player(x, y):
    screen.blit(playerImg, (x, y))


# enemy_function
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# weapon
def fire_arrow(x, y):
    global arrow_state
    arrow_state = "fire"
    screen.blit(arrowImg, (x, y + 10))


# collision
def isCollision(enemyX, enemyY, arrowX, arrowY):
    distance = math.sqrt(math.pow(enemyX - arrowX, 2) + math.pow(enemyY - arrowY, 2))
    if distance < 40:
        return True
    else:
        return False


# game loop
running = True
while running:

    # RGB = Red , green, blue
    screen.fill((245, 200, 66))

    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if a keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            #print("A keystroke has been pressed")

            if event.key == pygame.K_LEFT:
                # print("Left arrow is pressed")
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                # print("RIGHT arrow is pressed")
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                # get the current coordinate of the spaceship
                if arrow_state == "ready":
                    arrow_sound = mixer.Sound("laser.wav")
                    mixer.Sound.play(arrow_sound)
                    arrowX = playerX
                    fire_arrow(arrowX, arrowY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # print("keystroke has been released")
                playerX_change = 0
    # bounday checking
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    if playerX >= 737:
        playerX = 737
    for i in range(num_of_enemies):
        #Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >= 737:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]
        enemy(enemyX[i], enemyY[i], i)

        # collision check
        collision = isCollision(enemyX[i], enemyY[i], arrowX, arrowY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            mixer.Sound.play(explosion_sound)
            arrowY = 480
            arrow_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
    # arrow_movement
    if arrowY <= 0:
        arrowY = 480
        arrow_state = "ready"
    if arrow_state == "fire":
        fire_arrow(arrowX, arrowY)
        arrowY -= arrowY_change
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
