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
