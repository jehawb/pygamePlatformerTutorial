import math
import random

import pygame

from scripts.particle import Particle
from scripts.spark import Spark

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)    # Didn't quite understand this but helps with handling multiple entities in same position and dealing with tuplets
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        self.action = ''
        self.anim_offset = (-3, -3)   # Not all images in animation are the same size of the base image, this will counter act the difference in size
        self.flip = False   # The facing of the images of the entity
        self.set_action('idle')

        self.last_movement = [0, 0]

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        if action != self.action:   # No resetting the current action, let the animation run
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}   # Reset at every update

        # Can handle gravity aswell with velocity involved in the movement calculations
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        # Movement and associated physics
        # You want to keep the movement axis calculations separate
        self.pos[0] += frame_movement[0]    # X movement
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):   # Pushes the entity's rectangular to the collisions edge
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x     # Move the entity to it's rectangular, rects can't handle decimals and so can't do subpixel movement meaning they are not good for entitys general position as you'd only be able to move whole pixel widths.

        self.pos[1] += frame_movement[1]    # Y movement
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        # Flipping the image's facing using the horizontal movement
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        # Saves the last input for movement to be checked later
        self.last_movement = movement

        # Velocity from gravity with terminal velocity, min() picks the smaller one of the two parameters
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        # Stop the entity's vertical velocity if a vertical collision is detected
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        self.animation.update()

    # "offset" is for the camera
    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))

class Enemy(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'enemy', pos, size)

        self.walking = 0

    def update(self, tilemap, movement=(0, 0)):
        if self.walking:
            if tilemap.solid_check((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 23)):   # Checking seven pixels ahead and 23 below for solid ground
                if (self.collisions['right'] or self.collisions['left']):   # If running into something on right or left
                    self.flip = not self.flip
                else:
                    movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
            else:
                self.flip = not self.flip       # No solid ground found ahead, flip the entity
            self.walking = max(0, self.walking - 1)     # Reduing the walk timer
            if not self.walking:    # Shooting script, note that this is one frame window for this branch after the enemy has stopped walking
                dis = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1])
                if (abs(dis[1] < 16)):
                    if (self.flip and dis[0] < 0):  # If looking to left and player is to the left
                        self.game.sfx['shoot'].play()
                        self.game.projectiles.append([[self.rect().centerx - 7 , self.rect().centery], -1.5, 0])
                        for i in range(4):
                            # Location of the last projectile, -1 meaning one from the end, given as the initial location, also some randomization added to angle and speed
                            self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5 + math.pi, 2 + random.random()))
                    if (not self.flip and dis[0] > 0):
                        self.game.sfx['shoot'].play()
                        self.game.projectiles.append([[self.rect().centerx + 7 , self.rect().centery], 1.5, 0])
                        for i in range(4):
                            self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5, 2 + random.random()))
        elif random.random() < 0.01:                    # 1% chance of happening per frame -> game running at 60 fps means around every 1.6s
            self.walking = random.randint(30, 120)      # How long to walk for

        super().update(tilemap, movement=movement)

        if movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

        # Enemy hit while player is dashing
        if abs(self.game.player.dashing) >= 50:
            if self.rect().colliderect(self.game.player.rect()):
                self.game.screenshake = max(16, self.game.screenshake)
                self.game.sfx['hit'].play()
                for i in range(30):     # Sparks and particles on player hit
                            angle = random.random() * math.pi * 2   # Random angle in a circle
                            speed = random.random() * 5
                            self.game.sparks.append(Spark(self.rect().center, angle, 2 + random.random()))
                            self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
                self.game.sparks.append(Spark(self.rect().center, 0, 5 + random.random()))
                self.game.sparks.append(Spark(self.rect().center, math.pi, 5 + random.random()))
                return True

    # Used to render the weapon on top of the entity 
    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)

        if self.flip:
            surf.blit(pygame.transform.flip(self.game.assets['gun'], True, False), (self.rect().centerx - 4 - self.game.assets['gun'].get_width() - offset[0], self.rect().centery - offset[1]))   # Flips the gun and offsets it to fit the enemy better
        else:
            surf.blit(self.game.assets['gun'], (self.rect().centerx + 4 - offset[0], self.rect().centery - offset[1]))


# Player entity inheriting much of the general entity's functionality
class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        self.jumps = 1              # Number of jumps available for player, make sure you change the jump restoration aswell, currently in collision with the ground in update()
        self.wall_slide = False     # Wall sliding
        self.dashing = 0

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)

        # Setting the player actions for animations
        self.air_time += 1  # Weird implementation but OK, set right back to 0 if grounded

        # Handles the player falling off the screen
        if self.air_time > 120:
            if not self.game.dead:
                self.game.screenshake = max(16, self.game.screenshake)
            self.game.dead += 1  # Starts a sped up death timer
        
        # Grounding
        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 1      # Restores the jumps

        # Touching wall mid-air
        self.wall_slide = False
        if (self.collisions['right'] or self.collisions['left']) and self.air_time > 4:
            self.wall_slide = True
            self.velocity[1] = min(self.velocity[1], 0.5)   # Capping the downward velocity when wall sliding
            if self.collisions['right']:
                self.flip = False
            else:
                self.flip = True
            self.set_action('wall_slide')

        # Mid-air, running and idle animations overriden by wall slide
        if not self.wall_slide:
            if self.air_time > 4:
                self.set_action('jump')
            elif movement[0] != 0:
                self.set_action('run')
            else:
                self.set_action('idle')

        # Controlling the dashing
        if abs(self.dashing) in {60, 50}:   # For spawning some particles from player position when dashing starts OR ends
            for i in range(20):
                angle = random.random() * math.pi * 2
                speed = random.random() * 0.5 + 0.5
                pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]  # MATHEMATICAL! This makes the diagonal vectors same lenght as the horizontal and vertical ones
                self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))
        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)
        if abs(self.dashing) > 50:
            self.velocity[0] = abs(self.dashing) / self.dashing * 8     # First 10 frames of the dash give you velocity of 8
            if abs(self.dashing) == 51:
                self.velocity[0] *= 0.1     # After the first 10 frames of dash player is brought to stop, rest 50 frames are the cooldown for dash
                # Spawning some particles as player is dashing
            pvelocity = [abs(self.dashing) / self.dashing * random.random() * 3, 0]
            self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))

        # Brings the player to halt if moving automagically horizontally
        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)

    def render(self, surf, offset=(0, 0)):
        if abs(self.dashing) <= 50:     # Overriding the entity rendering if dashing
            super().render(surf, offset=offset)

    def jump(self):
        if self.wall_slide:
            if self.flip and self.last_movement[0] < 0:
                self.velocity[0] = 3.5  # Pushes player off the wall when jumping from wall_slide
                self.velocity[1] = -2.5 # Not the full jump force
                self.air_time = 5
                self.jumps = max(0, self.jumps -1)  # Can jump from the wall even if no jumps left, also consumes one jump
                return True     # Returns boolean for possible future checks
            elif not self.flip and self.last_movement[0] > 0:
                self.velocity[0] = -3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps -1)
                return True
        
        elif self.jumps:
            self.velocity[1] = -3   # Jumping makes player go up!
            self.jumps -= 1         # Jumping consumes jumps
            self.air_time = 5       # Jumping starts the jump animation
            return True

    def dash(self):
        if not self.dashing:
            self.game.sfx['dash'].play()
            if self.flip:
                self.dashing = -60
            else:
                self.dashing = 60