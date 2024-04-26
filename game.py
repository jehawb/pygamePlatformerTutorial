# A game made by following DaFluffyPotato's video tutorial: https://www.youtube.com/watch?v=2gABYM5M0ww
# !!! Get the 'data' folder from https://dafluffypotato.com/assets/pg_tutorial in the '00_resources.zip' file !!!

import sys
import pygame

from scripts.utils import load_image, load_images
from scripts.entities import PhysicsEntity
from scripts.tilemap import Tilemap

class Game:
    def __init__(self):

        # --- GAME SETUP ---

        pygame.init()

        # Text to be displayed on the window
        pygame.display.set_caption('ninja game')

        # Sets up the window and the rendering surface for the game, smaller rendering surface is upscaled to fit the window
        self.screen = pygame.display.set_mode((640, 480))   # The window for the game
        self.display = pygame.Surface((320, 240))           # The surface in the game for rendering stuff

        # Internal clock for the game loop ie. "fps"
        self.clock = pygame.time.Clock()

        # --- ENTITIES ---

        # Player entity
        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15))      # The third parameter is the starting position
        self.movement = [False, False]

        # Loading images for entities
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png')
        }

        # --- GAME MAP ---

        self.tilemap = Tilemap(self, tile_size=16)

    # --- GAMELOOP ---

    def run(self):

        # Gameloop, in this case everything in one loop, you could have one for fisiks, one for logic and so on
        while True:

            # --- RENDERING ---

            # Fills the whole screen with this color at the start of every frame to "clean", otherwise all moved sprites would leave traces 
            self.display.fill((14, 219, 248))

            self.tilemap.render(self.display)

            self.player.update((self.movement[1] - self.movement[0], 0))
            self.player.render(self.display)

            # --- INPUT READING ---

            # Gets the input and such, preventing the Windows thinking the program has stopped responding
            for event in pygame.event.get():

                # THE PART WHERE YOU PRESS THE "X" IN WINDOWS WINDOW TO QUIT THE PROGRAM, DO NOT FORGET!
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Reading the user input
                # Left and right movement
                if event.type == pygame.KEYDOWN:
                    # Left arrow key
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    # Right arrow key
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            # --- GAME STATE UPDATING ---

            # Renders the rendering surface on to the window and scale it up
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            # Updates the screen at the start of every loop or "frame"
            pygame.display.update()
            # Forces the loop to run at 60 fps
            self.clock.tick(60)

Game().run()