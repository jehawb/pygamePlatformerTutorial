import pygame

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

        # Velocity from gravity with terminal velocity, min() picks the smaller one of the two parameters
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        # Stop the entity's vertical velocity if a vertical collision is detected
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        self.animation.update()

    # "offset" is for the camera
    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))

# Player entity inheriting much of the general entity's functionality
class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)

        # Setting the player actions for animations
        self.air_time += 1  # Weird implementation but OK
        
        if self.collisions['down']:
            self.air_time = 0

        if self.air_time > 4:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')


