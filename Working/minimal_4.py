import pygame
import sys
from pygame.locals import *

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
# SCREEN_WIDTH, SCREEN_HEIGHT = get_monitor_size()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SIMPLE PANNING OF IMAGE")
clock = pygame.time.Clock()
fps = 60

# EXTRA OFFSET and PAN
world_offset_x, world_offset_y = 0, 0
panstart_x, panstart_y = 0.0, 0.0
world_scale = 1
world_scale_max = 4
zoomin = False
zoomout = False
panning = False

# SPRITESHEET
sprite_image = pygame.image.load("assets/copy.png").convert()
copy_image = sprite_image.copy()
sprite_image_pos = [0, 0]
sprite_image_rect = copy_image.get_rect(topleft=(0, 0))

# CAPTURE RECT
capture_rect = Rect([0, 0, 0, 0])  # Original data rect
capture_scale = 1
capture_gripping = False

# DEBUGGING
font = pygame.font.SysFont('Arial', 25, bold=True)
world_info = font.render(f"WORLD OFFSET - X : {world_offset_x} Y : {world_offset_y}", True, "Yellow")
sprite_info = font.render(f"SPRITE OFFSET - X : {sprite_image_pos[0]} Y : {sprite_image_pos[1]}", True, "Green")
capture_info = font.render("CAPTURE -    X :{} Y : {} W : {} H : {}".format(*capture_rect), True, "Orange")
panning_info = font.render(f"PANNING - {panning}", True, "White")
mousepos_info = font.render(f"MOUSE POS - X : {0} Y : {0}", True, "White")


# MOVEMENTS BY KEYS
ISDOWN = False
ISUP = False
ISLEFT = False
ISRIGHT = False
MOVESPEED = 2

############################################
# HELPER FUNCTIONS
def world_2_screen(world_x, world_y):
    """Convert world screen position to screen position"""
    screen_x = (world_x - world_offset_x) * world_scale
    screen_y = (world_y - world_offset_y) * world_scale
    return [screen_x, screen_y]

def screen_2_world(screen_x, screen_y):
    """Convert screen position to world screen position"""
    world_x = (screen_x / world_scale) + world_offset_x
    world_y = (screen_y / world_scale) + world_offset_y
    return [world_x, world_y]
############################################


# IG ARGUMENT DD ALWAYS AN ORIGINAL IMAGE
def capture_rect_detail(image_capture):
    """Capture sprite cleanly without the alpha color and
    trimmed properly as small as possible"""
    global capture_rect
    # Cache new rect
    try:
        # Cache a rect as local variable
        capturing_rect = Rect([0, 0, 0, 0])
        # capture alpha color of the image
        alpha_color = image_capture.get_at(capture_rect.topleft)
        other_color = False

        old_x = capture_rect.x + capture_rect.width
        for y in range(capture_rect.y, capture_rect.y + capture_rect.height, 1):
            for x in range(capture_rect.x, capture_rect.x + capture_rect.width, 1):
                if image_capture.get_at((x, y)) != alpha_color:
                    other_color = True
                    if x < old_x:
                        old_x = x
                        capturing_rect.x = x
                        break

        if other_color:
            old_x = capture_rect.x
            for y in range(capture_rect.y, capture_rect.y + capture_rect.height, 1):
                for x in range(capture_rect.x + capture_rect.width, capture_rect.x - 1, -1):
                    if image_capture.get_at((x, y)) != alpha_color:
                        if x > old_x:
                            old_x = x
                            if x > capture_rect.x:
                                capturing_rect.width = (x + 1) - capturing_rect.x
                            break

            old_y = capture_rect.y + capture_rect.height
            for x in range(capture_rect.x, capture_rect.x + capture_rect.width, 1):
                for y in range(capture_rect.y, capture_rect.y + capture_rect.height, 1):
                    if image_capture.get_at((x, y)) != alpha_color:
                        if y < old_y:
                            old_y = y
                            capturing_rect.y = y
                            break

            old_y = capture_rect.y
            for x in range(capture_rect.x, capture_rect.x + capture_rect.width, 1):
                for y in range(capture_rect.y + capture_rect.height, capture_rect.y - 1, -1):
                    if image_capture.get_at((x, y)) != alpha_color:
                        if y > old_y:
                            old_y = y
                            if y > capture_rect.y:
                                capturing_rect.height = (y + 1) - capturing_rect.y
                            break

            capture_rect = capturing_rect
        # return other_color
    except IndexError:
        # Cancel capture
        # out of bound pixel detected
        pass


def scale_image(image, image_scale):
    # CHECK LATER FOR BUG HERE
    return pygame.transform.scale(image, (image.get_width() * image_scale,
                                          image.get_height() * image_scale)).convert()


def scale_rect(new_scale, image_pos):
    global capture_rect, sprite_image_pos, world_scale
    # capture_rect.x -= image_pos[0]
    # capture_rect.y -= image_pos[1]
    # capture_rect.x = capture_rect.x / capture_scale
    # capture_rect.y = capture_rect.y / capture_scale
    # capture_rect.width = capture_rect.width / capture_scale
    # capture_rect.height = capture_rect.height / capture_scale
    # capture_rect.x = capture_rect.x * new_scale
    # capture_rect.y = capture_rect.y * new_scale
    # capture_rect.width = capture_rect.width * new_scale
    # capture_rect.height = capture_rect.height * new_scale
    # capture_rect.x += image_pos[0]
    # capture_rect.y += image_pos[1]
    # capture_scale = new_scale


###############################################
# DRAW FUNCTIONS
def draw_debugging():
    screen.blit(mousepos_info, (5, 380))
    screen.blit(panning_info, (5, 410))
    screen.blit(world_info, (5, 430))
    screen.blit(sprite_info, (5, 450))
    screen.blit(capture_info, (5, 470))

def draw_capturing_rect():
    pos = screen_2_world(0, 0)
    pos2 = screen_2_world(panstart_x, panstart_y)
    capture_rect.x = -pos[0] + 5
    capture_rect.y = -pos[1] + 5
    pygame.draw.rect(screen, "Yellow", capture_rect, 5)
###############################################

###############################################
# EVENT HANDLERS
def handle_key_movement(event):
    global ISDOWN, ISLEFT, ISRIGHT, ISUP
    if event.type == KEYDOWN:
        if event.key == K_DOWN:
            # sprite_image_pos[1] += 5
            # sprite_image_rect.y += 5
            # capture_rect.y += 5
            ISDOWN = True
        if event.key == K_UP:
            # sprite_image_pos[1] -= 5
            # sprite_image_rect.y -= 5
            # capture_rect.y -= 5
            ISUP = True
        if event.key == K_LEFT:
            # sprite_image_pos[0] -= 5
            # sprite_image_rect.x -= 5
            # capture_rect.x -= 5
            ISLEFT = True
        if event.key == K_RIGHT:
            # sprite_image_pos[0] += 5
            # sprite_image_rect.x += 5
            # capture_rect.x += 5
            ISRIGHT = True
    elif event.type == KEYUP:
        if event.key == K_DOWN:
            ISDOWN = False
        if event.key == K_UP:
            ISUP = False
        if event.key == K_LEFT:
            ISLEFT = False
        if event.key == K_RIGHT:
            ISRIGHT = False

def move_image():
    # MOVING
    if ISDOWN:
        sprite_image_pos[1] += MOVESPEED
        sprite_image_rect.y += MOVESPEED
        capture_rect.y += MOVESPEED
    if ISUP:
        sprite_image_pos[1] -= MOVESPEED
        sprite_image_rect.y -= MOVESPEED
        capture_rect.y -= MOVESPEED
    if ISLEFT:
        sprite_image_pos[0] -= MOVESPEED
        sprite_image_rect.x -= MOVESPEED
        capture_rect.x -= MOVESPEED
    if ISRIGHT:
        sprite_image_pos[0] += MOVESPEED
        sprite_image_rect.x += MOVESPEED
        capture_rect.x += MOVESPEED

def move_image_by_panning(event):
    global panstart_y, panstart_x, panning
    if event.type == MOUSEBUTTONDOWN:
        if event.button == 1:
            panstart_x = event.pos[0]
            panstart_y = event.pos[1]
            panning = True
    elif event.type == MOUSEBUTTONUP:
        if event.button == 1:
            panning = False

def move_image_panning(x, y):
    global world_offset_y, world_offset_x, panstart_y, panstart_x, world_scale
    if panning:
        world_offset_x -= (x - panstart_x) / world_scale
        world_offset_y -= (y - panstart_y) / world_scale
        panstart_x = x
        panstart_y = y

        pos = world_2_screen(0, 0)
        sprite_image_rect.x = pos[0]
        sprite_image_rect.y = pos[1]

        # c_pos = screen_2_world(x, y)
        # #c_pos_f = world_2_screen(c_pos[0], c_pos[1])
        # capture_rect.x = c_pos[0]
        # capture_rect.y = c_pos[1]

def handle_capturing_rect(event):
    global capture_gripping
    if event.type == MOUSEBUTTONDOWN:
        if event.button == 3:
            capture_rect.x, capture_rect.y = event.pos
            capture_rect.width = 0
            capture_rect.height = 0
            capture_gripping = True
    elif event.type == MOUSEBUTTONUP:
        if event.button == 3:
            # print("SPRITE CAPTOR UP")
            capture_gripping = False
###############################################

def main():
    global world_info, sprite_info, capture_info, panning_info, mousepos_info
    run = True
    while run:
        clock.tick(fps)
        events = pygame.event.get()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        ###################################
        # START OF FOR EVENT
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            handle_key_movement(event)

            handle_capturing_rect(event)

            # TODO: EXPERIMENTAL MOVING
            move_image_by_panning(event)

        # MOVE IMAGE BASED ON EVENTS CAPTURED
        move_image()
        #
        move_image_panning(mouse_x, mouse_y)



        # UPDATE DEBUGS
        world_info = font.render(f"WORLD OFFSET - X : {world_offset_x} Y : {world_offset_y}", True, "Yellow")
        sprite_info = font.render(f"SPRITE OFFSET - X : {sprite_image_rect.x} Y : {sprite_image_rect.y}", True, "Green")
        capture_info = font.render("CAPTURE -    X :{} Y : {} W : {} H : {}".format(*capture_rect), True, "Orange")
        panning_info = font.render(f"PANNING - {panning}", True, "White")
        mousepos_info = font.render(f"MOUSE POS - X : {panstart_x} Y : {panstart_y}", True, "White")
        # END OF FOR EVENT
        ###################################

        ###################################
        # EXTRA DRAW
        screen.fill("Black")
        screen.blit(copy_image, sprite_image_rect)
        draw_capturing_rect()


        # DEBUGGING
        draw_debugging()
        ###################################
        pygame.display.update()
        # END MAIN LOOP


if __name__ == "__main__":
    main()

