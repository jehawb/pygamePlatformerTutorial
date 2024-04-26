import pygame

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass', 'stone'}      # Faster to check random things from a set than from a list

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}           # Tiles on a grid, such as platforms
        self.offgrid_tiles = []     # Tiles not on a grid, such as background

        for i in range(10):
            # A horizontal line of grass tiles
            self.tilemap[str(3 + i) + ';10'] = {'type': 'grass', 'variant': 1, 'pos': (3 + i, 10)}
            # A vertical line of stone tiles
            self.tilemap['10;' + str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 5 + i)}

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
    def render(self, surf):
        for tile in self.offgrid_tiles:
            # No gridding for offgrid tiles
            surf.blit(self.game.assets[tile['type']][tile['variant']], tile['pos'])

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            # Renders the tile in specific location using it's type, variant and position. The position is multiplied with the tile size ie. tile grid size.
            # Asset loading is done in game.py
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))
