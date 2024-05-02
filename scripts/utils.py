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

# Animating images
class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.img_duration = img_dur     # How long to show one image in the animation
        self.loop = loop
        self.done = False
        self.frame = 0

    # Not 100% sure why this is needed, but it has something to do with the references to images
    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    # Moving the frame by one if reached the current image's duration cap, the animation is looping or last image of the animation
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images)) # Forces the images to loop around avoiding indexing errors
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
    
    # Returns the image to be rendered instead of rendering it for flexibility
    def img(self):
        return self.images[int(self.frame / self.img_duration)]