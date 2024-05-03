import pygame

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass', 'stone'}      # Faster to check random things from a set than from a list

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}           # Tiles on a grid, such as platforms
        self.offgrid_tiles = []     # Tiles not on a grid, such as background

        # # Creating a simple level for testing, DELETE WHEN NO LONGER NEEDED !!!
        # for i in range(10):
        #     # A horizontal line of grass tiles
        #     self.tilemap[str(3 + i) + ';10'] = {'type': 'grass', 'variant': 1, 'pos': (3 + i, 10)}
        #     # A vertical line of stone tiles
        #     self.tilemap['10;' + str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 5 + i)}

    # Checking the neighboring tiles for physics calculations, no need to check all of the tiles
    # Figure out where in the grid the given position is and get the neighbouring tiles if present
    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))      # Chopping off the decimals in consistent way
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    # More physics in entities.py
    # Checks to see if there is a tile with physics applied to it in the nearby tiles and creates a rectangular over it for physics calculations
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects

    # Off grid tiles rendered before on grid ones
    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            # No gridding for offgrid tiles
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        # Tiles are in a dictionary and checking up something from one is fast no matter how much stuff is in the dictionary
        # This means you can use it to render only the tiles that should ne on the screen akin to occlusion culling --> Optimization

        # Loops through all the tile places on the screen grid starting from top left
        # If a tile should be in the grid position, it is rendered
        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
