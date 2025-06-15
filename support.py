import os
import pygame

# Function to import all images from a folder and return them as a list of surfaces
# This function assumes that the images are in a format compatible with pygame (e.g., PNG, JPG)
def import_folder(path):
    surface_list = []
    for _, __, img_files in os.walk(path):
        for img_file in img_files:
            full_path = os.path.join(path, img_file)
            surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(surface)

    return surface_list