import pygame
import sys
from pygame.locals import *

pygame.init()

# Construct WORLD SPACE/SCREEN
SCREEN_WIDTH = 640
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
selectedcellX = 0
selectedcellY = 0
SelectCell = False


# Image to pan, move around
image = pygame.image.load("../Working/assets/copy.png").convert()
copy_image = image.copy()
pos_x = 0
pos_y = 0
panning = False
pan_start_pos = [0, 0]
image_rect = image.get_rect(topleft=(0, 0))

x_image = image.copy()
x_image_pos = x_image.get_rect()


font = pygame.font.SysFont('Arial', 25, bold=True)
rect_info = font.render("x:{}  y:{}  w:{}  h:{}".format(*image_rect), True, "Yellow")


def world_2_screen(world_x, world_y):
    screen_x = (world_x - world_offset_x) * scalex
    screen_y = (world_y - world_offset_y) * scaley
    return [screen_x, screen_y]


def screen_2_world(screen_x, screen_y):
    world_x = (screen_x / scalex) + world_offset_x
    world_y = (screen_y / scaley) + world_offset_y
    return [world_x, world_y]


circles = []

def add_circle(posx, posy):
    # CONVERT SCREEN MOUSE POS TO WORLD SPACE
    pos = screen_2_world(posx, posy)
    # circles.append([pos_x, pos_y])
    circles.append([pos[0], pos[1]])

def main():
    # Default screen/world space
    global world_offset_x, world_offset_y, panning, panstart_x, panstart_y, scalex, scaley, zoomin, zoomout, \
        selectedcellX, selectedcellY, SelectCell, rect_info
    # world_offset_x = -SCREEN_WIDTH / 2
    # world_offset_y = -SCREEN_HEIGHT / 2

    while True:
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
                    add_circle(mouse_x, mouse_y)
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

        # sprite_captor.scale_rect(scalex, [image_rect.x, image_rect.y])
            #
        mousebefore = screen_2_world(mouse_x, mouse_y)

        # Handle placing of circle in the screen
        if SelectCell:
            selectedcellX = mousebefore[0]
            selectedcellY = mousebefore[1]
            SelectCell = False
        if zoomin and scalex < 7:
            scalex += 1
            scaley += 1
            zoomin = False
        if zoomout and scalex > 1:
            scalex -= 1
            scaley -= 1
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

            # print(f"PANNING {panstart_x} : {panstart_y}")

            rect_info = font.render("x:{}  y:{}  w:{}  h:{}".format(*image_rect), True, "Yellow")

            # try update captor rect
            # sc_x, sc_y = sprite_captor.rect.x, sprite_captor.rect.y
            # spos = world_2_screen(sc_x, sc_y)
            # sprite_captor.rect.x = spos[0]
            # sprite_captor.rect.y = spos[1]

        screen.fill("Black")
        # draw square
        ############################################################
        # NADARA DIDI NA PART
        # KULANG NLA ITON ZOOMING HT IMAGE
        # rect_pos = world_2_screen(0, 0)
        # image_rect.x = rect_pos[0]
        # image_rect.y = rect_pos[1]
        # img = GuiSprite.scale_image(copy_image, scalex)

        rect_pos = world_2_screen(0, 0)
        # x_image_pos.x = rect_pos[0]
        # x_image_pos.y = rect_pos[1]
        # x_image_pos.h = img.get_height()
        # x_image_pos.w = img.get_width()

        # screen.blit(img, image_rect)
        screen.blit(rect_info, (5, 500 - 35))

        #pygame.draw.rect(screen, "Yellow", x_image_pos)



        pygame.draw.rect(screen, "Green", (rect_pos[0], rect_pos[1], 50 * scalex, 50 * scaley))
        ############################################################


        # Draw 10 vertical/horizontal lines
        x = 0
        for i in range(11):
            sx, sy = x, 0
            ex, ey = x, 0 + 100

            world_s = world_2_screen(sx, sy)
            world_e = world_2_screen(ex, ey)

            pygame.draw.line(screen, "Yellow", world_s, world_e, 1)
            x += 10
        y = 0
        for i in range(11):
            sx, sy = 0, y
            ex, ey = 0 + 100, y
            world_s = world_2_screen(sx, sy)
            world_e = world_2_screen(ex, ey)
            pygame.draw.line(screen, "Yellow", world_s, world_e, 1)
            y += 10

        # circlepos = world_2_screen(selectedcellX, selectedcellY)
        # cr = 0.1 * scalex
        # pygame.draw.circle(screen, "Red", circlepos, 5)
        #sprite_captor.draw(screen)

        # Draw Circles
        for c in circles:
            pos_x, pos_y = c[0], c[1]
            pos = world_2_screen(pos_x, pos_y)
            pygame.draw.circle(screen, "Red", [pos[0], pos[1]], 3)


        #screen.blit(copy_image, image_rect)
        pygame.display.update()



main()