# A game made by following DaFluffyPotato's video tutorial: https://www.youtube.com/watch?v=2gABYM5M0ww
# !!! Get the 'data' folder from https://dafluffypotato.com/assets/pg_tutorial in the '00_resources.zip' file !!!

import sys
import pygame

from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds

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

        # Loading images for entities
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
        }

        # Player entity
        self.player = Player(self, (50, 50), (8, 15))      # The third parameter is the starting position
        self.movement = [False, False]

        # --- GAME MAP ---

        self.clouds = Clouds(self.assets['clouds'], count=16)

        self.tilemap = Tilemap(self, tile_size=16)

        # --- CAMERA ---

        self.scroll = [0, 0]

    # --- GAMELOOP ---

    def run(self):

        # Gameloop, in this case everything in one loop, you could have one for fisiks, one for logic and so on
        while True:

            # --- RENDERING ---

            # Fills the whole screen with background image at the start of every frame to "clean", otherwise all moved sprites would leave traces 
            self.display.blit(self.assets['background'], (0, 0))

            # Moves the camera centering on the player with smoothing
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            # Removes the player character jitter releated to camera movement by removing decimal handling with casting to integer, camera "choppines" remains
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.tilemap.render(self.display, offset=render_scroll)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)

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
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3    # Jumping using the velocity

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