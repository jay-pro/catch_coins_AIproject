import pygame, os, random

here = os.path.dirname(os.path.abspath(__file__))
pygame.init()

# making the window
windowWidth = 900
windowHeight = 500
win = pygame.display.set_mode((windowWidth,windowHeight))
pygame.display.set_caption("i have no idea")

# load iamges
bg = pygame.image.load(os.path.join(here, 'sprites/game_background.jpg'))
walkRight = [pygame.image.load(os.path.join(here, 'sprites/run1_right.png')), pygame.image.load(os.path.join(here, 'sprites/run2_right.png')), pygame.image.load(os.path.join(here, 'sprites/run3_right.png')), pygame.image.load(os.path.join(here, 'sprites/run4_right.png')), pygame.image.load(os.path.join(here, 'sprites/run5_right.png')), pygame.image.load(os.path.join(here, 'sprites/run6_right.png')), pygame.image.load(os.path.join(here, 'sprites/run8_right.png'))]
walkLeft = [pygame.image.load(os.path.join(here, 'sprites/run1_left.png')), pygame.image.load(os.path.join(here, 'sprites/run2_left.png')), pygame.image.load(os.path.join(here, 'sprites/run3_left.png')), pygame.image.load(os.path.join(here, 'sprites/run4_left.png')), pygame.image.load(os.path.join(here, 'sprites/run5_left.png')), pygame.image.load(os.path.join(here, 'sprites/run6_left.png')), pygame.image.load(os.path.join(here, 'sprites/run8_left.png'))]
char = pygame.image.load(os.path.join(here, 'sprites/idle1.png'))
coinSprite = pygame.image.load(os.path.join(here, 'sprites/coin.png'))

# load sounds
coin_sound = pygame.mixer.Sound(os.path.join(here, 'sounds/coin_sound.wav'))
coin_sound.set_volume(0.10)

# class for a player
class player(object):

    # player constructor
    def __init__(self, x, y, width, height):
        self.xPos = x
        self.yPos = y
        self.width = width
        self.height = height

        self.vel = 10
        self.isJump = False
        self.jumpCount = 9
        self.left = False
        self.right = False
        self.walkCount = 0
        self.score = 0 

        self.hitbox = pygame.Rect(self.xPos + 20, self.yPos, 50, 85)

    # draw function to draw the player's sprites
    def draw(self, win):
        # initial walkCount is 0, and increments until equal to 70 then it resets to 0
        if self.walkCount + 1 >= 70:
            self.walkCount = 0

        # if the player is facing left, then display the walkLeft sprites, and increment walkCount
        if self.left:
            win.blit(walkLeft[self.walkCount//10], (self.xPos,self.yPos))
            self.walkCount += 1

        # if the player is facing right, then display the walkRight sprites, and increment walkCount
        elif self.right:
            win.blit(walkRight[self.walkCount//10], (self.xPos,self.yPos))
            self.walkCount += 1
    
        else:
            win.blit(char, (self.xPos, self.yPos))

        # when drawing the player, make sure to draw a hitbox around the player for collision purposes 
        self.hitbox = pygame.Rect(self.xPos + 20, self.yPos, 50, 85)
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)


# class for coin objects
class coin(object):

    # coin constructor
    def __init__(self, x, y, width, height, vel): 
        self.xPos = x
        self.yPos = y
        self.width = width
        self.height = height
        self.vel = vel
        self.hitbox = pygame.Rect(self.xPos, self.yPos, 50, 50)
    
    # draw function for coins
    def draw(self, win):


        self.yPos = self.yPos + self.vel
        if self.yPos > windowHeight:
            self.xPos = random.randrange(0,windowWidth-self.width)
            self.yPos = -25
        
        win.blit(coinSprite, (self.xPos, self.yPos))

        self.hitbox = pygame.Rect(self.xPos, self.yPos, 50, 50)
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

    def reset(self, win):
        self.xPos = random.randrange(0,windowWidth-self.width)
        self.yPos = -25 + self.vel

        win.blit(coinSprite, (self.xPos, self.yPos))

        self.hitbox = pygame.Rect(self.xPos, self.yPos, 50, 50)
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

# function to draw the game window
def drawGameWindow():

    #draw background
    win.blit(bg, (0,0))

    #draw object player
    character.draw(win)

    #make coins fall
    fastCoin.draw(win)
    slowCoin.draw(win)

    #update screen
    pygame.display.update()



# start of game loop
clock = pygame.time.Clock()

# creating a player object
character = player(50, 400, 100, 85)

# creating two coin objects that
fastCoin = coin(random.randrange(0, windowWidth), -25, 75, 75, 6)
slowCoin = coin(random.randrange(0,windowWidth), -25, 75, 75, 3)

running = True

# while running is true, run the game
while running:

    clock.tick(70)
    
    # for loop to continually get events, if user x's out, then running is false and stops the while loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    
    # any key pressed is a userinput
    userInput = pygame.key.get_pressed()

    # reading in arrow keys and keys a and d as left/right user input to control the character's x position
    if (userInput[pygame.K_a] or userInput[pygame.K_LEFT]) and character.xPos > character.vel:
        character.xPos -= character.vel
        character.left = True
        character.right = False
    elif userInput[pygame.K_RIGHT] or userInput[pygame.K_d] and character.xPos < windowWidth - character.width - character.vel:
        character.xPos += character.vel
        character.left = False
        character.right = True
    else:
        character.left = False
        character.right = False
        character.walkCount = 0

    # character can only move side to side    
    #if keys[pygame.K_UP] and y > vel:
    #    y-= vel
    #if keys[pygame.K_DOWN] and y < windowHeight - vel:
    #    y += vel

    # space key makes the player jump
    if not (character.isJump):
        if userInput[pygame.K_SPACE]:
            character.isJump = True

    # formula for jump position
    else:
        if character.jumpCount >= -9:
            neg = 1
            if character.jumpCount < 0:
                neg = -1
            character.yPos -= (character.jumpCount ** 2) * 0.5 * neg
            character.jumpCount -= 1
        else:
            character.isJump = False
            character.jumpCount = 9

    # character hitbox colliding with coin hit box
    if character.hitbox.colliderect(fastCoin.hitbox): 
        coin_sound.play()
        #character.score += 1
        #print(character.score)
        fastCoin.reset(win) 
    elif character.hitbox.colliderect(slowCoin.hitbox):
        coin_sound.play()
        #character.score += 1
        #print(character.score)
        slowCoin.reset(win)

        
    # updating the game window
    drawGameWindow()


# exit game loop 
pygame.quit()
