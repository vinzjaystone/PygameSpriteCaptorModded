import pygame
from pygame.locals import *
import sys
from Working.Util import SpriteCaptor

# SET PY GAME
pygame.init()
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SIMPLE PANNING OF IMAGE")
clock = pygame.time.Clock()
fps = 60

scale = 1
scale2 = 1
world_offset_x = 0
world_offset_y = 0
pan_start_x, pan_start_y = 0, 0
panning = False

image = pygame.image.load("../Working/assets/copy.png").convert()
copy_image = image.copy()
image_pos = [0, 0]
# image_rect = copy_image.get_rect(topleft=image_pos)

sprite_captor = SpriteCaptor.SpriteCaptor()

#######
# FOR DEBUGGING PURPOSES
font = pygame.font.SysFont('Arial', 25, bold=True)
imgpos_info = font.render(f"IMG X: {image_pos[0]} / IMG Y : {image_pos[1]}", True, "Yellow")
captor_info = font.render(f"CAPTOR X: {sprite_captor.rect.x} / CAPTOR Y : {sprite_captor.rect.y}", True, "Yellow")
offset_info = font.render(f"Offset X: {world_offset_x} / Offset Y : {world_offset_y}", True, "Yellow")
#######

def scale_image(img, sc):  # Scaling main image in main window
    return pygame.transform.scale(img, (img.get_width()*sc, img.get_height()*sc)).convert_alpha()


def world_2_screen(world_x, world_y):
    screen_x = int((world_x - world_offset_x) * scale2)
    screen_y = int((world_y - world_offset_y) * scale2)
    return [screen_x, screen_y]

def screen_2_world(screen_x, screen_y):
    world_x = int((screen_x / scale2) + world_offset_x)
    world_y = int((screen_y / scale2) + world_offset_y)
    return [world_x, world_y]


game = True
while game:
    clock.tick(fps)
    events = pygame.event.get()
    # cache mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    mousebefore = screen_2_world(mouse_x, mouse_y)
    mouseafter = screen_2_world(mouse_x, mouse_y)
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                pan_start_x = mouse_x
                pan_start_y = mouse_y
                panning = True
            # elif event.button == 4 or event.button == 5:
            #     if event.button == 4 and scale < 10:
            #         zoom_in = True
            #         # game_state.zoom *= scale_up
            #     elif event.button == 5 and scale > 1:
            #         zoom_out = True
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1 and panning is True:
                panning = False
        elif event.type == MOUSEWHEEL:
            if event.y == 1:
                if scale < 5:
                    scale += 1
                else:
                    scale = 5
                # image_move_speed = image_move_speed * scale
                copy_image = scale_image(image, scale)
                sprite_captor.scale_rect(scale, image_pos)
                # print("SCALING UP")
                mouseafter = screen_2_world(mouse_x, mouse_y)
            elif event.y == -1:
                if scale > 1:
                    scale -= 1
                else:
                    scale = 1
                # image_move_speed = image_move_speed * scale
                copy_image = scale_image(image, scale)
                sprite_captor.scale_rect(scale, image_pos)
                # print("SCALING DOWN")
                mouseafter = screen_2_world(mouse_x, mouse_y)
        sprite_captor.update(event, copy_image, image_pos)
    #

    sprite_captor.cycle_colors()

    # mousebefore = [mouse_x, mouse_y]
    # mouseafter = [mouse_x, mouse_y]

    world_offset_x += int(mousebefore[0] - mouseafter[0])
    world_offset_y += int(mousebefore[1] - mouseafter[1])

    new_x = int(pan_start_x - mouseafter[0])
    new_y = int(pan_start_y - mouseafter[1])

    if panning:
        world_offset_x -= int((mouse_x - pan_start_x))
        world_offset_y -= int((mouse_y - pan_start_y))
        pan_start_x = mouse_x
        pan_start_y = mouse_y

        new_pos = world_2_screen(0, 0)
        image_pos[0] = new_pos[0]
        image_pos[1] = new_pos[1]
        sprite_captor.rect.x = -new_pos2[0]
        sprite_captor.rect.y = -new_pos2[1]

        # image_pos[0] = new_x
        # image_pos[1] = new_y
        # sprite_captor.rect.x = new_x
        # sprite_captor.rect.y = new_y

        # rect_pos = world_2_screen(0, 0)
        # image_rect = copy_image.get_rect()
        # image_rect.x = rect_pos[0]
        # image_rect.y = rect_pos[1]

    imgpos_info = font.render(f"IMG X: {image_pos[0]} / IMG Y : {image_pos[1]}", True, "Yellow")
    captor_info = font.render(f"CAPTOR X: {sprite_captor.rect.x} / CAPTOR Y : {sprite_captor.rect.y}", True, "Yellow")
    offset_info = font.render(f"Offset X: {world_offset_x} / Offset Y : {world_offset_y}", True, "Yellow")

    screen.fill("Black")
    screen.blit(copy_image, image_pos)
    sprite_captor.draw(screen)

    screen.blit(imgpos_info, (0, 500))
    screen.blit(captor_info, (0, 550))
    screen.blit(offset_info, (5, 600))
    # Update scale

    # screen.blit(copy_image, image_rect)
    pygame.display.update()











