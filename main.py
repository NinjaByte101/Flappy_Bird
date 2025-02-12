import random
import sys
import pygame
from pygame.locals import *

FPS = 35
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8



GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = ("assets/sprites/bluebird-midflap.png")
BACKGROUND = ("assets/sprites/background-night.png")
PIPE = ("assets/sprites/pipe-red.png")

def welcomeScreen():

    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # if the user presses space or up key, start the game for then
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return 
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0,0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx,playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)
                
def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)                 
    playery = int(SCREENWIDTH/2)                 
    basex = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
     

    # my list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
    # my list of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerAccY = 1
    playerMaxVelY = 10
    playerMinVelY = -8

    playerFlapAccv = -8 # Velocity while flapping
    playerFlapped = True # it is true only when the bird is flapping


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerx,playery,upperPipes,lowerPipes) # This function will return true if the player is crashed
        if crashTest:
            return True

        # check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos + 4:
                score +=1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()


        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipse to the left
        for upperPipe , lowerpipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerpipe['x'] += pipeVelX

        # Add a new pipe when the first  is about to go to the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screeen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0,0))
        for upperPipe , lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerPipe['x'],lowerPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'],upperPipe['y']))
        
        SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx,playery,upperPipes,lowerPipes):
    if playery> GROUNDY - 25 or playery<0:
        GAME_SOUNDS['hit 2'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit 2'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx -pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit 2'].play()
            return True

    return False     

# def isCollide(playerx, playery, upperPipes, lowerPipes):
#     if playery > GROUNDY - GAME_SPRITES['player'].get_height() or playery < 0:
#         GAME_SOUNDS['hit 2'].play()
#         return True

#     playerRect = GAME_SPRITES['player'].get_rect()
#     playerRect.topleft = (playerx, playery)

#     for pipe in upperPipes:
#         pipeRect = GAME_SPRITES['pipe'][0].get_rect()
#         pipeRect.topleft = (pipe['x'], pipe['y'])
#         if playerRect.colliderect(pipeRect):
#             GAME_SOUNDS['hit 2'].play()
#             return True

#     for pipe in lowerPipes:
#         pipeRect = GAME_SPRITES['pipe'][1].get_rect()
#         pipeRect.topleft = (pipe['x'], pipe['y'])
#         if playerRect.colliderect(pipeRect):
#             GAME_SOUNDS['hit 2'].play()
#             return True

#     return False



def getRandomPipe():
    
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = int(SCREENHEIGHT / 3.5) 
    y2 = random.randrange(offset, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipeX = SCREENWIDTH + 10                                                              
    y1 = pipeHeight - y2 + offset
    pipe = [
        
        {'x': pipeX, 'y': -y2},  # Lower Pipe
        {'x': pipeX, 'y': y1},   # Upper Pipe
    
    ]
    return pipe

                               
if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy bird by Viren ')
    GAME_SPRITES['numbers'] = (
        pygame.image.load("assets/sprites/0.png").convert_alpha(),
        pygame.image.load("assets/sprites/1.png").convert_alpha(),
        pygame.image.load("assets/sprites/2.png").convert_alpha(),
        pygame.image.load("assets/sprites/3.png").convert_alpha(),
        pygame.image.load("assets/sprites/4.png").convert_alpha(),
        pygame.image.load("assets/sprites/5.png").convert_alpha(),
        pygame.image.load("assets/sprites/6.png").convert_alpha(),
        pygame.image.load("assets/sprites/7.png").convert_alpha(),
        pygame.image.load("assets/sprites/8.png").convert_alpha(),
        pygame.image.load("assets/sprites/9.png").convert_alpha(),
    )

    GAME_SPRITES['message'] = pygame.image.load("assets/sprites/message.png").convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load("assets/sprites/base.png").convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
    pygame.image.load(PIPE).convert_alpha()
    )


    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound("assets/Sounds/die.wav")
    GAME_SOUNDS['hit 2'] = pygame.mixer.Sound("assets/Sounds/hit.wav")
    GAME_SOUNDS['point'] = pygame.mixer.Sound("assets/Sounds/sfx_point.mp3")
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound("assets/Sounds/swoosh.wav")
    GAME_SOUNDS['wing'] = pygame.mixer.Sound("assets/Sounds/wing.wav")

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen()
        mainGame()
        
        