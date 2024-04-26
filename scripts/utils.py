import pygame

BASE_IMG_PATH = 'data/images/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()     # .convert() optimizes the image within pygame. Is magic, just do it.
    img.set_colorkey((0, 0, 0))
    return img