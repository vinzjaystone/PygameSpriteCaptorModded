import pygame
from pygame.locals import *

def scale_sprite2(image, scale):
    if scale != 0.25:
        img_w = image.get_width() * scale
        img_h = image.get_height() * scale
        new_w = int(image.get_width() + img_w)
        new_h = int(image.get_height() + img_h)
        return pygame.transform.scale(image, (new_w, new_h)).convert()
    else:
        return pygame.transform.scale(image, (image.get_width(), image.get_height())).convert()

def scale_sprite(image, scale):  # Scaling the sprite selected surface
    # sprite = image.subsurface(sprite_rect)
    # alpha = image.get_at((1, 1))
    # sprite.set_colorkey(alpha)
    return pygame.transform.scale(image, (image.get_width()*scale, image.get_height()*scale)).convert()

def scale_image(image, scale):  # Scaling main image in main window
    return pygame.transform.scale(image, (image.get_width()*scale, image.get_height()*scale)).convert_alpha()

def get_sprite_in_sheet(image, rect):
    sprite = image.subsurface(rect)
    alpha = image.get_at((1, 1))
    sprite.set_colorkey(alpha)
    x = pygame.transform.scale(sprite, (sprite.get_width() * 1, sprite.get_height() * 1)).convert_alpha()
    return x


    # return pygame.transform.flip(x, xbool=True)
    # return pygame.transform.scale(sprite, (sprite.get_width(), sprite.get_height())).convert()


class SpriteGUI(pygame.sprite.Sprite):
    """Default class for UI/GUI Sprite Editor"""
    def __init__(self, guid, image, pos, rect, handler=None):
        super().__init__()
        self.GUID = guid
        self.image = get_sprite_in_sheet(image, rect)

        ################
        # Adjust position to center at pixel/x 700 - 800
        start_x = 700 # position in x where i want to start
        width = self.image.get_width()
        new_x = (start_x - (width / 2))
        pos[0] = new_x
        ################
        self.rect = self.image.get_rect(topleft=pos)
        self.EventHandler = handler

    def update(self, ev: list):
        """Update only if event handler is set"""
        if self.EventHandler is not None:
            for e in ev:
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(e.pos):
                        self.EventHandler({'id': self.GUID})
