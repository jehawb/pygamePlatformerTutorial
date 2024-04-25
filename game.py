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

        # Loading an image to memory, does not render it on the screen, this is done in the gameloop
        self.img = pygame.image.load('data/images/clouds/cloud_1.png')
        # The image has a black background, with colorkey you can make it transparent
        self.img.set_colorkey((0, 0, 0))

        # For moving the image
        self.movement_speed = 5
        self.img_pos = [160, 260]
        self.movement = [False, False]

        # A rectangle for the collision physics testing
        self.collision_area = pygame.Rect(50, 50, 300, 50)

    def run(self):

        # Gameloop, in this case everything in one loop, you could have one for fisiks, one for logic and so on
        while True:

            # Fills the whole screen with this color at the start of every frame to "clean", otherwise all moved sprites would leave traces 
            self.screen.fill((14, 219, 248))

            # Collision rectangle for the image, created every frame as it is inside the gameloop
            img_r = pygame.Rect(self.img_pos[0], self.img_pos[1], self.img.get_width(), self.img.get_height())

            # Rendered layers in Pygame work in writing order, later in code are rendered on top of previous ones

            # Collision test
            if img_r.colliderect(self.collision_area):
                # Draw the rectangle if image collides with it with a blue color
                pygame.draw.rect(self.screen, (0, 100, 255), self.collision_area)
            else:
                # Draw the rectangle if image does not collide with it with a lighter blue color
                pygame.draw.rect(self.screen, (0, 50, 255), self.collision_area)

            # Updating the images position, with some python's boolean magic which deals if you hold down UP and DOWN simultaneously
            self.img_pos[1] += (self.movement[1] - self.movement[0]) * self.movement_speed
            # Renders the image from the loaded memory at the given coords, top-left is "0, 0"
            self.screen.blit(self.img, self.img_pos)

            # Gets the input and such, preventing the Windows thinking the program has stopped responding
            for event in pygame.event.get():

                # THE PART WHERE YOU PRESS THE "X" IN WINDOWS WINDOW TO QUIT THE PROGRAM, DO NOT FORGET!
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Reading the user input
                # Up and down movement
                if event.type == pygame.KEYDOWN:
                    # Up arrow key
                    if event.key == pygame.K_UP:
                        self.movement[0] = True
                    # Down arrow key
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.movement[0] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = False

            # Updates the screen at the start of every loop or "frame"
            pygame.display.update()
            # Forces the loop to run at 60 fps
            self.clock.tick(60)

Game().run()