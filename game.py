# A game made by following DaFluffyPotato's video tutorial: https://www.youtube.com/watch?v=2gABYM5M0ww
# !!! Get the 'data' folder from https://dafluffypotato.com/assets/pg_tutorial in the '00_resources.zip' file !!!

import sys
import pygame

class Game:
    def __init__(self):
        pygame.init()

        # Text to be displayed on the window
        pygame.display.set_caption('ninja game')

        # Sets up the window for the game
        self.screen = pygame.display.set_mode((640, 480))

        # Internal clock for the game loop ie. "fps"
        self.clock = pygame.time.Clock()

    def run(self):
        # Gameloop, in this case everything in one loop, you could have one for fisiks, one for logic and so on
        while True:
            # Gets the input and such, preventing the Windows thinking the program has stopped responding
            for event in pygame.event.get():
                # THE PART WHERE YOU PRESS THE 'X' IN WINDOWS WINDOW TO QUIT THE PROGRAM, DO NOT FORGET!
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Updates the screen at the start of every loop or "frame"
            pygame.display.update()
            # Forces the loop to run at 60 fps
            self.clock.tick(60)

Game().run()