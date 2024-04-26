import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)    # Didn't quite understand this but helps with handling multiple entities in same position and dealing with tuplets
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

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

        # Velocity from gravity with terminal velocity, min() picks the smaller one of the two parameters
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        # Stop the entity's vertical velocity if a vertical collision is detected
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

    def render(self, surf):
        surf.blit(self.game.assets['player'], self.pos)
