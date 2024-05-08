import json

import pygame

# Rules for autotiling, tile has neighbors which determine what the tile itself should look like, these are the neighbors which the neighbor search results are compared to
AUTOTILE_MAP = {
    # Sorted is used to make sure the neighbors are checked in consistent order, also list can't be used as a key -> tupling
    tuple(sorted([(1, 0), (0, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2,
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,   # This coulb be a typo
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,
}

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass', 'stone'}      # Faster to check random things from a set than from a list
AUTOTILE_TYPES = {'grass', 'stone'}

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}           # Tiles on a grid, such as platforms
        self.offgrid_tiles = []     # Tiles not on a grid, such as background

    # Find given tile's positions in offgrid tiles and ongrid tiles, used for particles for example
    def extract(self, id_pairs, keep=False):
        matches = []
        
        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy()) # Makes a copy of the tile so not to work with the original one
                if not keep:
                    self.offgrid_tiles.remove(tile)

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = matches[-1]['pos'].copy()  # Making a clean copy of the tile data for modification
                matches[-1]['pos'][0] *= self.tile_size
                matches[-1]['pos'][1] *= self.tile_size
                if not keep:
                    del self.tilemap[loc]
        
        return matches

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
    
    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f)
        f.close()   # This saves the file aswell

    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()

        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']
    
    # More physics in entities.py
    # Checks to see if there is a tile with physics applied to it in the nearby tiles and creates a rectangular over it for physics calculations
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    
    # Goes through all tiles on grid and checks their neighboring tiles to figure out how their variant should look
    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set()
            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                check_loc = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1])
                if check_loc in self.tilemap:   # Neighbor exists
                    if self.tilemap[check_loc]['type'] == tile['type']:     # Only tiles of same type are neighbors
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if (tile['type'] in AUTOTILE_TYPES) and (neighbors in AUTOTILE_MAP):    # Only autotile the types in AUTOTILE_TYPES ie. grass and stone as of now
                tile['variant'] = AUTOTILE_MAP[neighbors]

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
