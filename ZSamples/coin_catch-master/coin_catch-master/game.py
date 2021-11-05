import pygame
import models.palette as p
from models.game import Game

def main():
    # Pre-initialize the sound engine to reduce sound delay.
    pygame.mixer.pre_init(44100, -16, 1, 512)

    # Initialize the pygame engine.
    pygame.init()

    # Setup the main screen.
    main_screen = pygame.display.set_mode((700, 500))
    pygame.display.set_caption("Catch the Coins!")

    # Load background
    bg_image = pygame.image.load("assets/image/background.jpg").convert()

    # Create a Game instance.
    game = Game(main_screen, bg_image)

    # Meta variables.
    fps = 30
    clock = pygame.time.Clock()

    # Main game loop.
    while game.handle_events():
        clock.tick(fps)

        game.run_game_logic()

        game.display_frame()

    # Exit the Pygame engine.
    pygame.quit()

if __name__ == '__main__':
    main()