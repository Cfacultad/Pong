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
ball = {'rect':pygame.Rect(300, 80, 10, 10), 'color':WHITE, 'xVelocity': random.randint(2, 5), 'yVelocity': random.randint(2, 5) }

#Paddles
playerPaddle = {'rect':pygame.Rect(50, 225, 10, 40), 'color':WHITE }
aiPaddle = {'rect':pygame.Rect(550, 225, 10, 40), 'color':WHITE }

#Paddle movement
moveUp = False
moveDown = False

        
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
    ball['rect'].left -= ball['xVelocity']
    ball['rect'].top -= ball['yVelocity']

    #Paddle animation
    if moveUp == True:
        playerPaddle['rect'].top -= 5
    if moveDown == True:
        playerPaddle['rect'].top += 5
        
    #Ball Collision with Window
    #ball collides with top of window
    if ball['rect'].top < 0:
        ball['yVelocity'] -= ball['yVelocity'] * 2        
    # ball collides with bottom of window            
    if ball['rect'].bottom > WINDOW_HEIGHT:
        ball['yVelocity'] -= ball['yVelocity'] * 2
    # ball collides with left of window
    if ball['rect'].left < 0:
        ball['xVelocity'] -= ball['xVelocity'] * 2
    # ball collides with right of window
    if ball['rect'].right > WINDOW_WIDTH:
        ball['xVelocity'] -= ball['xVelocity'] * 2

    #Check if Ball has collided with paddle
    if ball['rect'].colliderect(playerPaddle['rect']):
        ball['xVelocity'] -= ball['xVelocity'] * 2
    if ball['rect'].colliderect(aiPaddle['rect']):
        ball['xVelocity'] -= ball['xVelocity'] * 2

    #AI
    if ball['rect'].left > WINDOW_WIDTH / 2: #AI reacts once ball passes halfway through screen
        if ball['rect'].top > aiPaddle['rect'].top: #AI follows the ball up if the ball is higher than the AI
            aiPaddle['rect'].top += 3
        if ball['rect'].top < aiPaddle['rect'].top: #AI follows the ball down if the lower is higher than the AI
            aiPaddle['rect'].top -= 3
    if ball['rect'].left < WINDOW_WIDTH / 4: #AI will recenter itself after its turn
        if WINDOW_HEIGHT / 2 > aiPaddle['rect'].top: 
            aiPaddle['rect'].top += 2
        if WINDOW_HEIGHT / 2 < aiPaddle['rect'].top: 
            aiPaddle['rect'].top -= 2

    
    #Draw paddles
    pygame.draw.rect(windowSurface, playerPaddle['color'], playerPaddle['rect'] )
    pygame.draw.rect(windowSurface, aiPaddle['color'], aiPaddle['rect'] )
    
    #Draw ball
    pygame.draw.rect(windowSurface, ball['color'], ball['rect'] )


    #Update frame
    pygame.display.update()
    time.sleep(0.02)
