import sys
import pygame

from scripts.utils import load_images
from scripts.tilemap import Tilemap

RENDER_SCALE = 2.0

class Editor:
    def __init__(self):

        pygame.init()

        pygame.display.set_caption('editor')
        self.screen = pygame.display.set_mode((640, 480))   
        self.display = pygame.Surface((320, 240))      

        self.clock = pygame.time.Clock()

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
        }

        self.movement = [False, False, False, False]

        self.tilemap = Tilemap(self, tile_size=16)

        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass

        self.scroll = [0, 0]

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True  # Wether to place a tile onto the collision tilemap grid or not

    def run(self):
        while True:
            self.display.fill((0, 0, 0))

            # Camera movement
            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2

            # Rendering
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            self.tilemap.render(self.display, offset=render_scroll)

            # Selecting the tile to be placed on to the level
            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()   # Make a copy of the tile so that you are not changing the original it refers to
            current_tile_img.set_alpha(100)

            # Mouse position
            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)     # The screen is not 1:1 so you must take this in account with mouse position aswell
            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size ), int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size))  # Aligns the tile_pos into the grid

            # Showing the place where to set the tile, taking account the grid snapping
            if self.ongrid:
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(current_tile_img, mpos)

            # Adding a tile on to the grid
            if self.clicking and self.ongrid:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos}
            
            # Deleting tiles
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:    # Position being right clicked "exists" in the tilemapping
                    del self.tilemap.tilemap[tile_loc]  # Deleting an ongrid tile
                for tile in self.tilemap.offgrid_tiles.copy():  # SYSTEM TAXING WAY TO, DELETE OFFGRID TILES
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height()) # Collision rectangles for every tile in the offgrid tilemap
                    if tile_r.collidepoint(mpos):   # Check if the created rectangle collides with point on mouse cursor
                        self.tilemap.offgrid_tiles.remove(tile)

            self.display.blit(current_tile_img, (5, 5))

            # --- INPUT READING ---

            for event in pygame.event.get():

                # System
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:   # LMB
                        self.clicking = True
                        if not self.ongrid: # Placing ONE offgrid tile (not on every frame)
                            self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])})
                    if event.button == 3:   # RMB
                        self.right_clicking = True
                    if self.shift == True:
                        if event.button == 4:   # Mouse scroll
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])     # Looping around trick with modulo
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:   # Mouse scroll
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0   # Prevents indexing erros if switching from high variant to group with not as many variants
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False
    
                # Keyboard
                # Sadly only WASD keyboards supported for the editor
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()
                    if event.key == pygame.K_o:
                        self.tilemap.save('map.json')
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False

            # --- RENDERING AND UPDATING ---
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Editor().run()