#import modules, 
import pygame, sys, time, random
from pygame.locals import*

pygame.init() #set up pygame

#Window
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 450

windowSurface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('Pong!')

#Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#Ball
ball = {'rect':pygame.Rect(300, 80, 10, 10), 'color':WHITE, 'xVelocity': random.randint(4, 6), 'yVelocity': random.randint(4, 6) }

#Paddles
playerPaddle = {'rect':pygame.Rect(50, 225, 10, 40), 'color':WHITE }
aiPaddle = {'rect':pygame.Rect(550, 225, 10, 40), 'color':WHITE }

#Paddle movement
moveUp = False
moveDown = False

#AI reaction time
aiReaction = 4.4

#Score Counter
player1 = 0
player2 = 0

#Pause
isPaused = False
def pause(duration):
    a = duration
    while a > 0:
        time.sleep(.5)
        a =- 1
        if (a == 0):
            isPaused = False
        else:
            isPaused = True
#Score
def score(winner, serveSide): #serveSide is either a -1 or 1. -1 meaning the ball moves to the left
        ball['xVelocity'] = 0
        ball['yVelocity'] = 0
        winner += 1
        pause(180)
        ball['rect'].left = 300
        ball['rect'].top = 80
        ball['xVelocity'] = random.randint(4, 6) * serveSide
        ball['yVelocity'] = random.randint(3, 6)
        playerPaddle['rect'].top = WINDOW_HEIGHT / 2
        aiPaddle['rect'].top = WINDOW_HEIGHT / 2

#Debug reset
def debug():
        ball['rect'].left = 300
        ball['rect'].top = 80
        ball['xVelocity'] = random.randint(4, 6)
        ball['yVelocity'] = random.randint(3, 6)
        playerPaddle['rect'].top = WINDOW_HEIGHT / 2
        aiPaddle['rect'].top = WINDOW_HEIGHT / 2
        
while True: #game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            # change the keyboard variables
            if event.key == K_w:
                moveDown = False
                moveUp = True
            if event.key == K_s:
                moveUp = False
                moveDown = True
            if event.key == K_d:
                debug()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_w:
                moveUp = False
            if event.key == K_s:
                moveDown = False
                

    #Draw Blackground
    windowSurface.fill(BLACK)

    #Ball animation
    if isPaused == False:
        ball['rect'].left -= ball['xVelocity']
        ball['rect'].top -= ball['yVelocity']

    #Paddle animation
    if moveUp == True & isPaused == False:
        playerPaddle['rect'].top += 5
    if moveDown == True & isPaused == False:
        playerPaddle['rect'].top -= 5
        
    #Ball Collision with Window
    #ball collides with top of window
    if ball['rect'].top < 0:
        ball['yVelocity'] -= ball['yVelocity'] * 2        
    # ball collides with bottom of window            
    if ball['rect'].bottom > WINDOW_HEIGHT:
        ball['yVelocity'] -= ball['yVelocity'] * 2

    #Check if Ball has collided with paddle
    if ball['rect'].colliderect(playerPaddle['rect']):
        ball['xVelocity'] -= ball['xVelocity'] * 2
    if ball['rect'].colliderect(aiPaddle['rect']):
        ball['xVelocity'] -= ball['xVelocity'] * 2

    #AI
    if ball['rect'].left > WINDOW_WIDTH / 2: #AI reacts once ball passes halfway through screen
        if ball['rect'].top > aiPaddle['rect'].top: #AI follows the ball up if the ball is higher than the AI
            aiPaddle['rect'].top += aiReaction
        if ball['rect'].top < aiPaddle['rect'].top: #AI follows the ball down if the lower is higher than the AI
            aiPaddle['rect'].top -= aiReaction
    if ball['rect'].left < WINDOW_WIDTH / 4: #AI will recenter itself after its turn
        if WINDOW_HEIGHT / 2 > aiPaddle['rect'].top: 
            aiPaddle['rect'].top += aiReaction - 2
        if WINDOW_HEIGHT / 2 < aiPaddle['rect'].top: 
            aiPaddle['rect'].top -= aiReaction - 2
            
    #Score Detection
    #Player Score
    if ball['rect'].left >= WINDOW_WIDTH:
        score(player1, -1)
        
    #AI Score
    if ball['rect'].left <= 0:
        score(player2, 1)

    
    #Draw paddles
    pygame.draw.rect(windowSurface, playerPaddle['color'], playerPaddle['rect'] )
    pygame.draw.rect(windowSurface, aiPaddle['color'], aiPaddle['rect'] )
    
    #Draw ball
    pygame.draw.rect(windowSurface, ball['color'], ball['rect'] )


    #Update frame
    pygame.display.update()
    time.sleep(0.02)
