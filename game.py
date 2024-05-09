# A game made by following DaFluffyPotato's video tutorial: https://www.youtube.com/watch?v=2gABYM5M0ww
# !!! Get the 'data' folder from https://dafluffypotato.com/assets/pg_tutorial in the '00_resources.zip' file !!!

import sys
import random
import math

import pygame

from scripts.spark import Spark
from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player, Enemy
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle

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
            'enemy/idle': Animation(load_images('entities/enemy/idle'), img_dur=6),
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=4),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
            'gun': load_image('gun.png'),
            'projectile': load_image('projectile.png'),
        }

        # Player entity
        self.player = Player(self, (50, 50), (8, 15))      # The third parameter is the starting position
        self.movement = [False, False]

        # --- GAME MAP ---

        self.clouds = Clouds(self.assets['clouds'], count=16)

        self.tilemap = Tilemap(self, tile_size=16)
        
        self.load_level(0)

    def load_level(self, map_id):
        self.tilemap.load('data/maps/' + str(map_id) + '.json')

        # --- PARTICLES ---

        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))  # Rectangle here in this size makes sense for the tree tile

        # --- ENTITY SPAWNERS ---

        self.enemies = []

        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))

        # --- LISTS FOR SMALL STUFF ---

        self.projectiles = []
        self.particles = []
        self.sparks = []

        # --- CAMERA ---

        self.scroll = [0, 0]

        # --- PLAYER ENTITY STATE ---

        self.dead = 0

    # --- GAMELOOP ---

    def run(self):

        # Gameloop, in this case everything in one loop, you could have one for fisiks, one for logic and so on
        while True:

            # --- RENDERING ---
            # Later rendered entities overlap the previously rendered

            # Fills the whole screen with background image at the start of every frame to "clean", otherwise all moved sprites would leave traces 
            self.display.blit(self.assets['background'], (0, 0))

            # Player death
            if self.dead:   # Timer starts after player death
                self.dead += 1
                if self.dead > 40:      # Loading level 0 after 40 frames of death
                    self.load_level(0)

            # Moves the camera centering on the player with smoothing
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            # Removes the player character jitter releated to camera movement by removing decimal handling with casting to integer, camera "choppines" remains
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:   # Generate random number and compare it to the spawner's size so bigger spawners get spawn more particles, 49999 affects spawn rate per frame
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)   # Randomizes the position within the spawner
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[0.05, 0.3], frame=random.randint(0, 20)))   # Randomizes the starting leaf frame aswell, AFAIK not working atm the moment

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.tilemap.render(self.display, offset=render_scroll)

            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset=render_scroll)
                if kill:
                    self.enemies.remove(enemy)

            if not self.dead:   # No player rendering if dead
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)

            # Outline for projectile[[x, y], direction, timer]
            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]   # Adding the projectile speed to the projectile's x-axis position
                projectile[2] += 1                  # Adding to the projectile timer
                img = self.assets['projectile']
                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
                if self.tilemap.solid_check(projectile[0]):     # Deleting the projectile if hitting wall
                    self.projectiles.remove(projectile)
                    for i in range(4):
                            # Sparks to the opposing direction of projectile
                            self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))
                elif projectile[2] > 360:                       # Deleting the projectile if timing out in 6s
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:             # Player can dash through projectiles
                    if self.player.rect().collidepoint(projectile[0]):      # Deleting the projectile if hitting player
                        self.projectiles.remove(projectile)
                        self.dead += 1
                        for i in range(30):     # Sparks and particles on player hit
                            angle = random.random() * math.pi * 2   # Random angle in a circle
                            speed = random.random() * 5
                            self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
                            self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))

            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset=render_scroll)
                if kill:
                    self.sparks.remove(spark)

            # Particle management
            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3     # Gives leaves sine curve patch 
                if kill:
                    self.particles.remove(particle) # Remove particles with animation played out

            # --- INPUT READING ---

            # Gets the input and such, preventing the Windows thinking the program has stopped responding
            for event in pygame.event.get():

                # THE PART WHERE YOU PRESS THE "X" IN WINDOWS WINDOW TO QUIT THE PROGRAM, DO NOT FORGET!
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Reading the user input
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.jump()      # Jumping using the function
                    if event.key == pygame.K_x:
                        self.player.dash()

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