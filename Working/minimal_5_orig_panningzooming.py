import pygame
import sys
from pygame.locals import *

# REMARKS:
'''
PANNING AND ZOOMING -> WORKING
ADDING BOX/RECT IN SCREEN -> WORKING
ABLE TO MOVE/ZOOM BOX IN SCREEN -> WORKING
ADDING BOX SELECTING IN SPRITE -> WIP
'''

# TODO: Make this main panning and zooming file template

pygame.init()

# Construct WORLD SPACE/SCREEN
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


pygame.display.set_caption("SIMPLE PANNING OF IMAGE")
clock = pygame.time.Clock()
fps = 60

# EXTRA OFFSET
world_offset_x = -300
world_offset_y = -300
panstart_x = 0
panstart_y = 0
panning = False
scalex = 1
scaley = 1
zoomin = False
zoomout = False
selectedcellX = 0
selectedcellY = 0
SelectCell = False


# Image to pan, move around
pos_x = 0
pos_y = 0
pan_start_pos = [0, 0]


sprite_image = pygame.image.load("assets/copy.png").convert()
copy_image = sprite_image.copy()
sprite_image_pos = [0, 0]

def scale_image(image, image_scale):
    # CHECK LATER FOR BUG HERE
    return pygame.transform.scale(image, (image.get_width() * image_scale,
                                          image.get_height() * image_scale)).convert()

def world_2_screen(world_x, world_y):
    screen_x = (world_x - world_offset_x) * scalex
    screen_y = (world_y - world_offset_y) * scaley
    return [screen_x, screen_y]


def screen_2_world(screen_x, screen_y):
    world_x = (screen_x / scalex) + world_offset_x
    world_y = (screen_y / scaley) + world_offset_y
    return [world_x, world_y]


circles = []



box = []
pos = [0, 0]
gripping = False

capture_rect = Rect([0, 0, 0, 0])
def draw_sprite_image():
    global pos
    s_x, s_y = sprite_image_pos[0], sprite_image_pos[1]
    pos = world_2_screen(s_x, s_y)
    screen.blit(copy_image, (pos[0], pos[1]))

def add_circle(posx, posy):
    global capture_rect
    # CONVERT SCREEN MOUSE POS TO WORLD SPACE
    pos = screen_2_world(posx, posy)
    # circles.append([pos_x, pos_y])
    print(f"POSITION IS : {pos}")
    circles.append([pos[0], pos[1]])

    rect = Rect([pos[0], pos[1], 50, 90])
    print(f"RECT IS : {rect}")

    # capture_rect.x = pos[0]
    # capture_rect.y = pos[1]
    box.append(rect)
    # capture_rect = Rect([0, 0, 0, 0])

    # handle_rect_capturing_old(posx, posy)


def handle_rect_capturing_new(posx, posy):
    global gripping, capture_rect
    new_pos = screen_2_world(posx, posy)



def handle_rect_capturing(event):
    """
    Needs Reprogram
    dapat an ma offset it position
    :param event: events tikang h pygame get evets()
    """
    global gripping, capture_rect
    # Summary
    #: On mouse down
    #:  - get mouse position
    #:  - convert mouse pos to screen_2_world
    #:  - set cache capture_rect x & y position to converted mouse position
    #: On monitor mouse motion for rect width & height
    #:  - set rect's width and height via rect's x and y set on mouse down
    #
    #: to draw convert position.x and position.y again to world_2_screen

    # On Mouse Down
    if event.type == MOUSEBUTTONDOWN:
        if event.button == 3:
            mouse_x, mouse_y = event.pos
            new_pos = screen_2_world(mouse_x, mouse_y)
            capture_rect.x, capture_rect.y = new_pos[0], new_pos[1]
            gripping = True
    elif event.type == MOUSEBUTTONUP:
        if event.button == 3:
            gripping = False
            box.append(capture_rect.copy())
            capture_rect = Rect([0, 0, 0, 0])
    elif event.type == MOUSEMOTION:
        if gripping:
            # CHECK LATER DINHE KUN MYDA ERROR HA SCALING
            mouse_x, mouse_y = event.pos
            new_pos = screen_2_world(mouse_x, mouse_y)
            capture_rect.width = new_pos[0] - capture_rect.x
            capture_rect.height = new_pos[1] - capture_rect.y


    #
    # global gripping
    # if event.type == MOUSEBUTTONDOWN:
    #     if event.button == 3:
    #         print("SPRITE CAPTOR DOWN")
    #         capture_rect.x, capture_rect.y = event.pos
    #         capture_rect.width = 0
    #         capture_rect.height = 0
    #         gripping = True
    # elif event.type == MOUSEBUTTONUP:
    #     if event.button == 3:
    #         print("SPRITE CAPTOR UP")
    #         gripping = False
    #         if capture_rect.width < 0:
    #             capture_rect.width *= -1
    #             capture_rect.x -= capture_rect.width
    #         if capture_rect.height < 0:
    #             capture_rect.height *= -1
    #             capture_rect.y -= capture_rect.height
    #
    #         s_x, s_y = event.pos[0], event.pos[1]
    #         pos = world_2_screen(s_x, s_y)
    #
    #         copy_image_rect = copy_image.get_rect()
    #         copy_image_rect.topleft = pos
    #
    #         # check for overflow
    #         if capture_rect.right > capture_rect.right \
    #                 or capture_rect.left < copy_image_rect.left \
    #                 or capture_rect.bottom > copy_image_rect.bottom \
    #                 or capture_rect.top < copy_image_rect.top:
    #             capture_rect.topleft = copy_image_rect.topleft
    #             capture_rect.size = (0, 0)
    #             #  Na rereset it rect dinhe kun it selection rect is gawas hit image
    #         capture_rect.x -= pos[0]
    #         capture_rect.y -= pos[1]
    #         # capture_rect_detail(copy_image)
    #         capture_rect.x += pos[0]
    #         capture_rect.y += pos[1]
    #
    #         box.append(capture_rect.copy())
    # if event.type == MOUSEMOTION:
    #     if gripping:
    #         # CHECK LATER DINHE KUN MYDA ERROR HA SCALING
    #         capture_rect.width = event.pos[0] - capture_rect.x
    #         capture_rect.height = event.pos[1] - capture_rect.y
    #
    #         print(f"Width : {capture_rect.width}  Height : {capture_rect.height}")


def handle_mouse(event):
    """
        Needs Reprogram
        dapat an ma offset it position
        :param event: events tikang h pygame get evets()
        """
    global gripping, capture_rect
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if event.type == MOUSEBUTTONDOWN:
        if event.button == 3:
            new_pos = screen_2_world(mouse_x, mouse_y)
            capture_rect.x, capture_rect.y = new_pos[0], new_pos[1]
            gripping = True
    elif event.type == MOUSEBUTTONUP:
        if event.button == 3:
            gripping = False
            box.append(capture_rect)
            capture_rect = Rect([0, 0, 0, 0])
    elif event.type == MOUSEMOTION:
        if gripping:
            # CHECK LATER DINHE KUN MYDA ERROR HA SCALING
            new_pos = screen_2_world(mouse_x, mouse_y)
            capture_rect.width = new_pos[0] - capture_rect.x
            capture_rect.height = new_pos[1] - capture_rect.y

def main():
    global world_offset_x, world_offset_y, \
        panning, panstart_x, panstart_y, scalex, \
        scaley, zoomin, zoomout, selectedcellX, \
        selectedcellY, SelectCell, sprite_image_pos, copy_image, pos
    #print(f"INITIAL POSITION : {pos}")
    while True:
        #print(f"CURRENT POSITION : {pos}")
        clock.tick(fps)
        events = pygame.event.get()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in events:

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    panstart_x = mouse_x
                    panstart_y = mouse_y
                    panning = True
                elif event.button == 3:
                    pass
                elif event.button == 4 or event.button == 5:
                    if event.button == 4 and scalex < 10:
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
                    add_circle(mouse_x, mouse_y)
                # handle_mouse(event)
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    zoomin = True
                elif event.key == K_e:
                    zoomout = True
            elif event.type == KEYUP:
                if event.key == K_q and zoomin is True:
                    zoomin = False
                elif event.key == K_e and zoomout is True:
                    zoomout = False
            #
            # handle_rect_capturing(event)
        mousebefore = screen_2_world(mouse_x, mouse_y)


        # Handle placing of circle in the screen
        if SelectCell:
            selectedcellX = mousebefore[0]
            selectedcellY = mousebefore[1]
            SelectCell = False
        if zoomin and scalex < 10:
            scalex += 1
            scaley += 1
            copy_image = scale_image(sprite_image, scalex)
            zoomin = False
        if zoomout and scalex > 1:
            scalex -= 1
            scaley -= 1
            copy_image = scale_image(sprite_image, scalex)
            zoomout = False

        mouseafter = screen_2_world(mouse_x, mouse_y)

        # Adjust offset after mouse change
        world_offset_x += (mousebefore[0] - mouseafter[0])
        world_offset_y += (mousebefore[1] - mouseafter[1])
        if panning:
            world_offset_x -= (mouse_x - panstart_x) / scalex
            world_offset_y -= (mouse_y - panstart_y) / scaley
            panstart_x = mouse_x
            panstart_y = mouse_y

        screen.fill("Black")
        rect_pos = world_2_screen(0, 0)
        pygame.draw.rect(screen, "Green", (rect_pos[0], rect_pos[1], 50 * scalex, 50 * scaley))
        ############################################################

        draw_sprite_image()

        # # Draw 10 vertical/horizontal lines
        # x = 0
        # for i in range(11):
        #     sx, sy = x, 0
        #     ex, ey = x, 0 + 100
        #
        #     world_s = world_2_screen(sx, sy)
        #     world_e = world_2_screen(ex, ey)
        #
        #     pygame.draw.line(screen, "Yellow", world_s, world_e, 1)
        #     x += 10
        # y = 0
        # for i in range(11):
        #     sx, sy = 0, y
        #     ex, ey = 0 + 100, y
        #     world_s = world_2_screen(sx, sy)
        #     world_e = world_2_screen(ex, ey)
        #     pygame.draw.line(screen, "Yellow", world_s, world_e, 1)
        #     y += 10
        #
        # Draw Circles
        for c in circles:
            posx, posy = c[0], c[1]
            pos = world_2_screen(posx, posy)
            pygame.draw.circle(screen, "Red", [pos[0], pos[1]], 3)
            pygame.draw.rect(screen, "Black", [pos[0], pos[1], 10*scalex, 2*scaley], 2)
            # pygame.draw.rect(screen, "Black", [pos[0], pos[1], 50*scalex, 50*scaley], 3)

        # for b in box:
        #     r = b
        #     posx, posy = r.x, r.y
        #     pos = world_2_screen(posx, posy)
        #     pygame.draw.circle(screen, "Pink", [pos[0], pos[1]], 6)
            # pygame.draw.rect(screen, "Black", [pos[0], pos[1], 5, 5], 1)

        pygame.display.update()


main()
