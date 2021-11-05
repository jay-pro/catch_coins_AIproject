# -*- coding: utf-8 -*-
"""
Created on Mon May 02 20:56:30 2016

Simple game where the player has to dodge the asteroids (grey) and catch the
golden coins (yellow). When playing as a human, hold the mouse button to move 
left or leave it to move right.

The idea is to create a simple environment for training a deep (convolutional)
neural network. The CNN will be coded and published at a later stage.

Feel free to code your own agent. You need to:
1) create a class Agent in file CNN_Agent.py (in the same folder as this game);
2) implement a method self.__init__ that accepts SCREEN_WIDTH (int) as input;
3) implement a method self.choose_action(image, reward, is_terminal)
that accepts:
    - image: array, image made of raw pixels captured from the game screen;
    - reward: float, reward received at that particular state;
    - is_terminal: bool, indicates if the player is at a terminal state;
and returns:
    - (+1) for right move, (0) for no move, and (-1) for left move;
4) implement a method self.close() that clears the graph of Tensorflow.

@author: Riccardo Rossi
"""

# Fix the screen's size. The screen will be a rectangle with sizes
# (SCREEN_WIDTH) x (SCREEN_WIDTH + MARGIN_FOR_FONT)
SCREEN_WIDTH = 504
MARGIN_FOR_FONT = 36
SCREEN_HEIGHT = SCREEN_WIDTH + MARGIN_FOR_FONT

import pygame
import time
import numpy as np
np.random.seed(int(time.time()))
import matplotlib.pyplot as plt

# Hyperparameters
HUMAN_PLAYING = False
ACTION_STEPS = 4   # Steps to observe before deciding next action
PLAYER_SPEED = 6
GOLD_SPEED = 6
OBSTACLE_SPEED = 6
REWARD_CATCHING_GOLD = 1.
PLAYER_DIES_PENALTY = 0.
PROB_OBJECT_SPAWNED = 0.12
# Probability gold is spawned conditional to an object being spawned
PROB_GOLD_SPAWNED = 0.8

# Try to import Tensorflow and initialize the CNN agent
# If unsuccessful, it sets the game as played by a human
if not HUMAN_PLAYING:
    try:
        import tensorflow as tf
        from tensorflow.python.framework import ops
        import CNN_Agent
        agent = CNN_Agent.Agent(SCREEN_WIDTH)
    except:
        print('It was not possible to load TensorFlow. The human will play.')
        HUMAN_PLAYING = True

GAME_TITLE = 'Asteroids - dodge the asteroids (grey), catch the gold (yellow)'
TPS = 100             
FRAME_WIDTH = 3
FRAME_FROM_BORDER = 3

# Loose definition of a colours used in the game
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (219, 218, 191)
GOLD = (255, 215, 64)
GREY = (112, 138, 127)

class Block(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()


class Player(Block):
    def __init__(self, colour=RED, width=30, height=18):
        Block.__init__(self, width, height)
        self.image.fill(colour)
        self.rect.x = int((SCREEN_WIDTH/2 - width) / 6)*6
        self.rect.y = SCREEN_HEIGHT - height - 18
        self.score = 0
        self.speed = [+PLAYER_SPEED, 0]

    def is_position_allowed(self):
        if (self.rect.right > SCREEN_WIDTH - FRAME_FROM_BORDER - FRAME_WIDTH or 
            self.rect.x < FRAME_FROM_BORDER + FRAME_WIDTH):
            return(False)
        if (self.rect.bottom > SCREEN_HEIGHT - FRAME_FROM_BORDER - FRAME_WIDTH 
            or self.rect.y < FRAME_FROM_BORDER + FRAME_WIDTH):
            return(False)
        return(True)

    def move(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

    def update(self):
        self.move()


class Asteroid(Block):
    def __init__(self, colour=GREY, width=12, height=12, speed=OBSTACLE_SPEED):
        Block.__init__(self, width, height)
        self.image.fill(colour)
        self.rect.x = int(np.random.randint(
            FRAME_FROM_BORDER + FRAME_WIDTH, 
            SCREEN_WIDTH - FRAME_FROM_BORDER - FRAME_WIDTH - width)/6)*6
        self.rect.y = FRAME_FROM_BORDER + FRAME_WIDTH
        self.speed = speed
    
    def update(self):
        self.rect.y += self.speed
        

class Gold(Block):
    def __init__(self, colour=GOLD, width=12, height=12, speed=GOLD_SPEED):
        Block.__init__(self, width, height)
        self.image.fill(colour)
        self.rect.x = int(np.random.randint(
            FRAME_FROM_BORDER + FRAME_WIDTH, 
            SCREEN_WIDTH - FRAME_FROM_BORDER - FRAME_WIDTH - width)/6)*6
        self.rect.y = FRAME_FROM_BORDER + FRAME_WIDTH
        self.speed = speed

    def update(self):
        self.rect.y += self.speed


start = time.time()         # Useful for measuring the duration of the game
###############################################################################

# Launch PyGame
pygame.init()
pygame.display.set_caption(GAME_TITLE)
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

all_items_list = pygame.sprite.Group()
player_list = pygame.sprite.Group()
obstacle_list = pygame.sprite.Group()
gold_list = pygame.sprite.Group()

player = Player()
player_list.add(player)
all_items_list.add(player)

# Initialize a few useful variables
font = pygame.font.SysFont("calibri",20)
reward = max_score = last_score = 0
is_terminal = inquire_the_agent = False
count = action = +1
clock = pygame.time.Clock()

# Start the game
running = True
while running:    

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False            
            continue

        if HUMAN_PLAYING:
            if (event.type == pygame.MOUSEBUTTONDOWN or 
                event.type == pygame.MOUSEBUTTONUP):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    action = -1
                if event.type == pygame.MOUSEBUTTONUP:
                    action = 1

    # Update all items' positions and the game_count    
    all_items_list.update() 
    count += 1
       
    # Create the background, basic frame, and score line
    screen.fill(BLACK)
    frame = pygame.draw.rect(screen, WHITE, pygame.Rect(
                (FRAME_FROM_BORDER, FRAME_FROM_BORDER),
                (SCREEN_WIDTH - 2*FRAME_FROM_BORDER, 
                 SCREEN_HEIGHT - 2*FRAME_FROM_BORDER)), 
                 FRAME_WIDTH)
    score = font.render('Max score : ' + 
                        str(int(max_score)) + 
                        ';      Last score : ' + 
                        str(int(last_score)) + 
                        ';      Current score : ' + 
                        str(int(player.score)), True, WHITE)
    screen.blit(score, (FRAME_FROM_BORDER + FRAME_WIDTH + 6, 
                        FRAME_FROM_BORDER + FRAME_WIDTH))

    # Generate obstacles and golden coins randomly
    if ((not obstacle_list and not gold_list) or
        np.random.uniform() < PROB_OBJECT_SPAWNED):    
        if np.random.uniform() < PROB_GOLD_SPAWNED:
            gold = Gold()
            gold_list.add(gold)
            all_items_list.add(gold)
        else:
            asteroid = Asteroid()
            obstacle_list.add(asteroid)
            all_items_list.add(asteroid)

    # Count the elements caught by the player 
    obstacle_hits = pygame.sprite.spritecollide(player, obstacle_list, True)
    gold_hits = pygame.sprite.spritecollide(player, gold_list, True)

    # If gold was caught by the player, then reward is distributed
    if gold_hits:
        reward = REWARD_CATCHING_GOLD * len(gold_hits)
        player.score += reward
        inquire_the_agent = True

    # Remove all elements that hit the bottom frame
    for elem in list(obstacle_list) + list(gold_list):
        if elem.rect.bottom > SCREEN_HEIGHT - FRAME_FROM_BORDER - FRAME_WIDTH:
            elem.kill()

    # If the player hits an obstacle or the screen's border, it's game over
    # The scores are updated and the game is reset
    if obstacle_hits or not player.is_position_allowed():
        last_score = player.score
        if max_score < player.score: 
            max_score = player.score
            
        all_items_list.empty()
        player_list.empty()
        obstacle_list.empty()
        gold_list.empty()
        is_terminal = True 
        inquire_the_agent = True
        reward += PLAYER_DIES_PENALTY
        
        player = Player()
        player_list.add(player)
        all_items_list.add(player)
    else:
        is_terminal = False

    # Print all objects in the screen
    all_items_list.draw(screen)
    pygame.display.flip()
    clock.tick(TPS)

    if count % ACTION_STEPS == 0:
        inquire_the_agent = True

    # Inquire the Agent               
    if not HUMAN_PLAYING and inquire_the_agent:     
        image = pygame.surfarray.array3d(screen)
        image = image[:, MARGIN_FOR_FONT:, :]

        # Agent's action function has to return +1 for right and -1 for left
        action = agent.choose_action(image, reward, is_terminal)
        
        inquire_the_agent = False
        reward = 0.0

    player.speed = [+PLAYER_SPEED * action, 0]

# Save settings, reset the graph, and close the session
if not HUMAN_PLAYING:
    agent.close()
del font, score; pygame.display.quit(); pygame.quit()

###############################################################################
print ('Max score was', max_score)
print('The process took :', round(time.time() - start, 2), 'seconds')

