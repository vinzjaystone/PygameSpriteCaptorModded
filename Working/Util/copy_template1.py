import pygame
import sys
from pygame.locals import *
from Working.Util import SpriteCaptor

pygame.init()
# Construct WORLD SPACE/SCREEN
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("SIMPLE PANNING OF IMAGE")
clock = pygame.time.Clock()
fps = 30
# EXTRA OFFSET
world_offset_x = 0
world_offset_y = 0
panstart_x = 0
panstart_y = 0
scalex = 1
scaley = 1
zoomin = False
zoomout = False

# Image to pan, move around
img_pos = [0, 0]
pos_x = 0
pos_y = 0
panning = False
pan_start_pos = [0, 0]

# - SPRITE CAPTOR -
image = pygame.image.load("../assets/M_Swordsman.png").convert()
copy_image = image.copy()
image_pos = [0, 0]
sprite_captor = SpriteCaptor.SpriteCaptor()
# - SPRITE CAPTOR -

font = pygame.font.SysFont('Arial', 25, bold=True)
# rect_info = font.render("x:{}  y:{}  w:{}  h:{}".format(*image_rect), True, "Yellow")


def world_2_screen(world_x, world_y):
    """Convert world screen position to screen position"""
    screen_x = int((world_x - world_offset_x) * scalex)
    screen_y = int((world_y - world_offset_y) * scaley)
    return [screen_x, screen_y]


def screen_2_world(screen_x, screen_y):
    """Convert screen position to world screen position"""
    world_x = int((screen_x / scalex) + world_offset_x)
    world_y = int((screen_y / scaley) + world_offset_y)
    return [world_x, world_y]

def scale_image2(img, scale):
    _width = img.get_width()
    _height = img.get_height()
    return pygame.transform.scale(copy_image, (_width * scalex, _height * scaley)).convert()

def draw_image():
    global image, image_pos, sprite_captor
    image_pos = world_2_screen(0, 0)
    screen.blit(copy_image, image_pos)
    sprite_captor.draw(screen)

    # img = image.subsurface([11, 110, 40, 73])
    # screen.blit(img, (250, 500))

def main():
    # Default screen/world space
    global world_offset_x, world_offset_y, panning, panstart_x, panstart_y, scalex, scaley, zoomin, zoomout, \
        selectedcellX, selectedcellY, SelectCell, rect_info, copy_image, image_rect, image_pos

    while True:
        clock.tick(fps)
        events = pygame.event.get()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # FOR START
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    panstart_x = mouse_x
                    panstart_y = mouse_y
                    panning = True
                elif event.button == 4 or event.button == 5:
                    if event.button == 4 and scalex < 4:
                        zoomin = True
                        # game_state.zoom *= scale_up
                    elif event.button == 5 and scalex > 1:
                        zoomout = True
                        # game_state.zoom *= scale_down
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1 and panning is True:
                    panning = False
                elif event.button == 3:
                    SelectCell = True
            # elif event.type == KEYDOWN:
            #     if event.key == K_q:
            #         zoomin = True
            #     elif event.key == K_e:
            #         zoomout = True
            # elif event.type == KEYUP:
            #     if event.key == K_q and zoomin is True:
            #         zoomin = False
            #     elif event.key == K_e and zoomout is True:
            #         zoomout = False
            sprite_captor.update(event, copy_image, image_pos)
        # END FOR
        sprite_captor.cycle_colors()

        # -- START ZOOMING --
        mousebefore = screen_2_world(mouse_x, mouse_y)
        if zoomin and scalex < 4:
            scalex += 1
            scaley += 1
            zoomin = False
            # Scale viewing sprite
            copy_image = scale_image2(image, scalex)
            sprite_captor.scale_rect(scalex, image_pos)
            # Reset captor rect
            # Dire ko pa na aayad an kun ma zoom ako hn sprite an size
            # and position hn captor is ma adjust based hn scale
            # so yana reset la anay an rect
            sprite_captor.reset()
        if zoomout and scalex > 1:
            scalex -= 1
            scaley -= 1
            zoomout = False
            # Scale viewing sprite
            copy_image = scale_image2(image, scalex)
            sprite_captor.scale_rect(scalex, image_pos)
            # Reset captor rect
            # Dire ko pa na aayad an kun ma zoom ako hn sprite an size
            # and position hn captor is ma adjust based hn scale
            # so yana reset la anay an rect
            sprite_captor.reset()
        mouseafter = screen_2_world(mouse_x, mouse_y)
        # Adjust offset after mouse change
        world_offset_x += (mousebefore[0] - mouseafter[0])
        world_offset_y += (mousebefore[1] - mouseafter[1])
        # -- END ZOOMING --

        mouseafter = [mouse_x, mouse_y]
        new_x = panstart_x - mouseafter[0]
        new_y = panstart_y - mouseafter[1]

        # -- START PANNING --
        if panning:
            world_offset_x -= (mouse_x - panstart_x) / scalex
            world_offset_y -= (mouse_y - panstart_y) / scaley
            panstart_x = mouse_x
            panstart_y = mouse_y
            print("Panning")

            sprite_captor.rect.x -= new_x
            sprite_captor.rect.y -= new_y

            # sprite_captor.reset()
        # -- END PANNING --

        screen.fill("Black")
        draw_image()
        pygame.display.update()


main()
