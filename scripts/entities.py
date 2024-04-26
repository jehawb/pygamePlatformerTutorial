import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)    # Didn't quite understand this but helps with handling multiple entities in same position and dealing with tuplets
        self.size = size
        self.velocity = [0, 0]

    def update(self, movement=(0, 0)):
        # Can handle gravity aswell with velocity involved in the movement calculations
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])


        self.pos[0] += frame_movement[0]    # X movement
        self.pos[1] += frame_movement[1]    # Y movement

        # Velocity from gravity with terminal velocity, min() picks the smaller one of the two parameters
        self.velocity[1] = min(5, self.velocity[1] + 0.1)
        
    def render(self, surf):
        surf.blit(self.game.assets['player'], self.pos)
