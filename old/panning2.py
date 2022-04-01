import pygame
from pygame.locals import *
import sys

# SET PY GAME
pygame.init()
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SIMPLE PANNING OF IMAGE")
clock = pygame.time.Clock()
fps = 60

scale = 1
zoomin = False
zoomout = False
world_offset_x = 0
world_offset_y = 0
pan_start_x, pan_start_y = 0, 0
panning = False

image = pygame.image.load("hero_sakari.png").convert()
copy_image = image.copy()
image_pos = [0, 0]
image_rect = copy_image.get_rect(topleft=image_pos)

# sprite_captor = SpriteCaptor.SpriteCaptor()
#######
# FOR DEBUGGING PURPOSES
font = pygame.font.SysFont('Arial', 25, bold=True)
imgpos_info = font.render(f"IMG X: {image_pos[0]} / IMG Y : {image_pos[1]}", True, "Yellow")
# captor_info = font.render(f"CAPTOR X: {sprite_captor.rect.x} / CAPTOR Y : {sprite_captor.rect.y}", True, "Yellow")
offset_info = font.render(f"Offset X: {world_offset_x} / Offset Y : {world_offset_y}", True, "Yellow")
#######

def scale_image(img, sc):  # Scaling main image in main window
    return pygame.transform.scale(img, [int(img.get_width()*sc), int(img.get_height()*sc)]).convert_alpha()

def world2screen(x, y):
    screen_x = int((x - world_offset_x) * scale)
    screen_y = int((y - world_offset_y) * scale)
    return [screen_x, screen_y]

def screen2world(x, y):
    world_x = int((x / scale) + world_offset_x)
    world_y = int((y / scale) + world_offset_y)
    return [world_x, world_y]


game = True
while game:
    clock.tick(fps)
    events = pygame.event.get()
    # cache mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # mouse_before = screen2world(mouse_x, mouse_y)
    # mouse_after = screen2world(mouse_x, mouse_y)
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                pan_start_x = mouse_x
                pan_start_y = mouse_y
                panning = True
            elif event.button == 4 or event.button == 5:
                if event.button == 4 and scale < 10:
                    zoomin = True
                    # game_state.zoom *= scale_up
                elif event.button == 5 and scale > 1:
                    zoomout = True
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1 and panning is True:
                panning = False
        # # SCALING
        # elif event.type == MOUSEWHEEL:
        #     # Capture mouse pos before zoom
        #     mouse_before = screen2world(mouse_x, mouse_y)
        #     if event.y == 1:
        #         if scale < 4:
        #             scale += 1
        #         else:
        #             scale = 4
        #         copy_image = scale_image(image, scale)
        #     elif event.y == -1:
        #         if scale > 1:
        #             scale -= 1
        #         else:
        #             scale = 1
        #         copy_image = scale_image(image, scale)
        #     mouse_after = screen2world(mouse_x, mouse_y)
        #
        #     # Update new offset after zooming
        #     world_offset_x += int(mouse_before[0] - mouse_after[0])
        #     world_offset_y += int(mouse_before[1] - mouse_after[1])

    mousebefore = screen2world(mouse_x, mouse_y)
    if zoomin and scale < 6:
        scale += 1
        zoomin = False
        copy_image = scale_image(image, scale)
    if zoomout and scale > 1:
        scale -= 1
        zoomout = False
        copy_image = scale_image(image, scale)
    mouseafter = screen2world(mouse_x, mouse_y)
    world_offset_x += (mousebefore[0] - mouseafter[0])
    world_offset_y += (mousebefore[1] - mouseafter[1])

    if panning:
        world_offset_x -= int((mouse_x - pan_start_x) / scale)
        world_offset_y -= int((mouse_y - pan_start_y) / scale)
        pan_start_x = mouse_x
        pan_start_y = mouse_y
        offset_info = font.render(f"Offset X: {world_offset_x} / Offset Y : {world_offset_y}  Scale : {scale}", True, "Yellow")

    # Update image position

    screen.fill("Black")
    screen.blit(copy_image, [-world_offset_x, -world_offset_y])
    screen.blit(offset_info, [5, 200])
    pygame.display.update()

