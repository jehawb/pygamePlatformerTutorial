import os
import pygame

BASE_IMG_PATH = 'data/images/'

# Loading a single image
def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()     # .convert() optimizes the image within pygame. Is magic, just do it.
    img.set_colorkey((0, 0, 0))
    return img

# Loading multiple images
def load_images(path):
    images = []
    # Loads the images from the folder and the order is important so index 0 is the 0.png, sorted() helps with non-Windows OSs
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images