"""
sprite.py - contains sprite classes derived from the pygame.sprite.Sprite class.
"""
import pygame
import random


class Paddle(pygame.sprite.Sprite):
    """
    A player-controlled paddle.
    """
    def __init__(self, img: pygame.Surface, screen: pygame.Surface):
        """
        Creates a new Paddle object.

        Args:
            img: A pygame.Surface image loaded through pygame.image.load
            screen: A pygame.Surface where the Paddle is to be drawn.
        """
        super().__init__()
        self.screen = screen

        # Create the Paddle surface.
        width, height = img.get_width(), img.get_height()
        self.image = pygame.Surface((width, height))
        self.image.blit(img, (0, 0))

        # Save the dimensions to the rect attribute.
        self.rect = self.image.get_rect()

        self.x_speed = 0


    def update(self):
        self.rect.x += self.x_speed

        # Prevent going out of bounds.
        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x >= self.screen.get_width() - self.image.get_width():
            self.rect.x = self.screen.get_width() - self.image.get_width()


class Coin(pygame.sprite.Sprite):
    """
    A coin that drops from a random place at the top of the screen.
    """
    def __init__(self, img: pygame.Surface, sound: pygame.mixer.Sound, screen: pygame.Surface):
        """
        Creates a new Coin object.

        Args:
            img: A pygame.Surface image loaded through pygame.image.load
            screen: A pygame.Surface where the Coin is to be drawn.
        """
        super().__init__()
        self.screen = screen
        self.sound = sound

        # Create the Coin surface.
        width, height = img.get_width(), img.get_height()
        self.image = pygame.Surface((width, height))
        self.image.blit(img, (0, 0))

        # Save the dimensions to the rect attribute.
        self.rect = self.image.get_rect()

        self.y_speed = 3

    
    def update(self):
        self.rect.y += self.y_speed

        # Respawn coin when it dropped out of bounds.
        if self.rect.y >= self.screen.get_height() + self.image.get_height():
            self.reset()

    def reset(self):
        self.rect.x = random.randrange(self.screen.get_width() - self.image.get_width())
        self.rect.y = random.randrange(-(self.screen.get_height() // 2), 0)
