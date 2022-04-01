import pygame
import sys
from pygame.locals import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
# SCREEN_WIDTH, SCREEN_HEIGHT = get_monitor_size()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SIMPLE PANNING OF IMAGE")
clock = pygame.time.Clock()
fps = 60

# EXTRA OFFSET and PAN
world_offset_x, world_offset_y = 0.0, 0.0
panstart_x, panstart_y = 0.0, 0.0
scale = 1
scale_max = 5
zoomin = False
zoomout = False
panning = False

# SPRITESHEET
sprite_image = pygame.image.load("assets/copy.png").convert()
copy_image = sprite_image.copy()
sprite_image_pos = [0, 0]


# CAPTURE RECT
capture_rect = Rect([0, 0, 0, 0])  # Original data rect
capture_scale = 1
capture_gripping = False

def mouse_2_image(x, y, pan_x, pan_y):
    _x = (x - pan_x) * scale
    _y = (y - pan_y) * scale
    return [_x, _y]

def world_2_screen(world_x, world_y):
    """Convert world screen position to screen position"""
    screen_x = (world_x - world_offset_x) * scale
    screen_y = (world_y - world_offset_y) * scale
    return [screen_x, screen_y]

def screen_2_world(screen_x, screen_y):
    """Convert screen position to world screen position"""
    world_x = (screen_x / scale) + world_offset_x
    world_y = (screen_y / scale) + world_offset_y
    return [world_x, world_y]

def scale_sprite_rect():
    pass

def scale_image(image, image_scale):
    # CHECK LATER FOR BUG HERE
    return pygame.transform.scale(image, (image.get_width() * image_scale,
                                          image.get_height() * image_scale)).convert()

def capture_rect_detail(copy):
    global capture_rect
    # Cache new rect
    try:
        capturing_rect = Rect([0, 0, 0, 0])
        alpha_color = copy.get_at(capture_rect.topleft)
        other_color = False

        old_x = capture_rect.x + capture_rect.width
        for y in range(capture_rect.y, capture_rect.y + capture_rect.height, 1):
            for x in range(capture_rect.x, capture_rect.x + capture_rect.width, 1):
                if copy.get_at((x, y)) != alpha_color:
                    other_color = True
                    if x < old_x:
                        old_x = x
                        capturing_rect.x = x
                        break
        if other_color:
            old_x = capture_rect.x
            for y in range(capture_rect.y, capture_rect.y + capture_rect.height, 1):
                for x in range(capture_rect.x + capture_rect.width, capture_rect.x - 1, -1):
                    if copy.get_at((x, y)) != alpha_color:
                        if x > old_x:
                            old_x = x
                            if x > capture_rect.x:
                                capturing_rect.width = (x + 1) - capturing_rect.x
                            break

            old_y = capture_rect.y + capture_rect.height
            for x in range(capture_rect.x, capture_rect.x + capture_rect.width, 1):
                for y in range(capture_rect.y, capture_rect.y + capture_rect.height, 1):
                    if copy.get_at((x, y)) != alpha_color:
                        if y < old_y:
                            old_y = y
                            capturing_rect.y = y
                            break

            old_y = capture_rect.y
            for x in range(capture_rect.x, capture_rect.x + capture_rect.width, 1):
                for y in range(capture_rect.y + capture_rect.height, capture_rect.y - 1, -1):
                    if copy.get_at((x, y)) != alpha_color:
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

def scale_rect(new_scale, image_pos):
    global capture_rect, sprite_image_pos, scale, capture_scale
    capture_rect.x -= image_pos[0]
    capture_rect.y -= image_pos[1]
    capture_rect.x = capture_rect.x / capture_scale
    capture_rect.y = capture_rect.y / capture_scale
    capture_rect.width = capture_rect.width / capture_scale
    capture_rect.height = capture_rect.height / capture_scale
    capture_rect.x = capture_rect.x * new_scale
    capture_rect.y = capture_rect.y * new_scale
    capture_rect.width = capture_rect.width * new_scale
    capture_rect.height = capture_rect.height * new_scale
    capture_rect.x += image_pos[0]
    capture_rect.y += image_pos[1]
    capture_scale = new_scale

def capture_rect_draw():
    pygame.draw.rect(screen, "Yellow", capture_rect, 5)

def handle_scaling(event):
    global scale, copy_image, sprite_image, zoomin, zoomout
    if event.type == MOUSEBUTTONDOWN:
        if event.button == 4 or event.button == 5:
            if event.button == 4 and scale < scale_max:
                zoomin = True
            elif event.button == 5 and scale > 1:
                zoomout = True


    # if event.type == MOUSEWHEEL:
    #     old_scale = scale
    #     if event.y == 1:
    #         zoomin = True
    #         # if scale < scale_max:
    #         #     scale += 1
    #         # else:
    #         #     scale = scale_max
    #     elif event.y == -1:
    #         zoomout = True
    #         # if scale > 1:
    #         #     scale -= 1
    #         # else:
    #         #     scale = 1
    #     # Update scale of copy_image only if changed
    #     # if scale != old_scale:
    #     #     # scale image first
    #     #     copy_image = scale_image(sprite_image, scale)
    #     #     # scale capturing rect if there is
    #     #     scale_rect(scale, sprite_image_pos)
    #     #     # scale_rect2(scale, sprite_image_pos)

def handle_rect_capturing(event):
    global capture_gripping
    if event.type == MOUSEBUTTONDOWN:
        if event.button == 3:
            print("SPRITE CAPTOR DOWN")
            if event.pos[0] < 600:
                capture_rect.x, capture_rect.y = event.pos
                capture_rect.width = 0
                capture_rect.height = 0
                capture_gripping = True
    elif event.type == MOUSEBUTTONUP:
        if event.button == 3:
            print("SPRITE CAPTOR UP")
            capture_gripping = False
            if capture_rect.width < 0:
                capture_rect.width *= -1
                capture_rect.x -= capture_rect.width
            if capture_rect.height < 0:
                capture_rect.height *= -1
                capture_rect.y -= capture_rect.height

            copy_image_rect = copy_image.get_rect()
            copy_image_rect.topleft = sprite_image_pos

            # check for overflow
            if capture_rect.right > capture_rect.right \
                    or capture_rect.left < copy_image_rect.left \
                    or capture_rect.bottom > copy_image_rect.bottom \
                    or capture_rect.top < copy_image_rect.top:
                capture_rect.topleft = copy_image_rect.topleft
                capture_rect.size = (0, 0)
                #  Na rereset it rect dinhe kun it selection rect is gawas hit image
            capture_rect.x -= sprite_image_pos[0]
            capture_rect.y -= sprite_image_pos[1]
            """#capture the whole image if we get nothing
            if not self.capture_sprite(image):
               self.rect.topleft = (0,0)
               self.rect.width = image.get_width() - 1
               self.rect.height = image.get_height() - 1
               self.capture_sprite(image)"""

            capture_rect_detail(copy_image)
            capture_rect.x += sprite_image_pos[0]
            capture_rect.y += sprite_image_pos[1]

    if event.type == MOUSEMOTION:
        if capture_gripping:
            # CHECK LATER DINHE KUN MYDA ERROR HA SCALING
            capture_rect.width = event.pos[0] - capture_rect.x
            capture_rect.height = event.pos[1] - capture_rect.y

            print(f"Width : {capture_rect.width}  Height : {capture_rect.height}")

def handle_panning(event):
    global panstart_y, panstart_x, panning
    if event.type == MOUSEBUTTONDOWN:
        if event.button == 1:
            panstart_x = event.pos[0]
            panstart_y = event.pos[1]
            panning = True
    elif event.type == MOUSEBUTTONUP:
        if event.button == 1:
            panning = False

def main():
    global panning, panstart_x, panstart_y, scale, world_offset_x, world_offset_y, sprite_image_pos, capture_rect
    global zoomin, zoomout, copy_image
    running = True
    while running:
        clock.tick(fps)
        events = pygame.event.get()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # FOR START
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # Process capturing rect and scaling
            handle_panning(event)
            handle_scaling(event)
            handle_rect_capturing(event)


        #
        mousebefore = screen_2_world(mouse_x, mouse_y)
        # Do Zooming
        if zoomin and scale < scale_max:
            scale += 1
            copy_image = scale_image(sprite_image, scale)
            # scale capturing rect if there is
            scale_rect(scale, sprite_image_pos)
            # scale_rect2(scale, sprite_image_pos)
            zoomin = False
        if zoomout and scale > 1.0:
            scale -= 1
            copy_image = scale_image(sprite_image, scale)
            # scale capturing rect if there is
            scale_rect(scale, sprite_image_pos)
            # scale_rect2(scale, sprite_image_pos)
            zoomout = False
        mouseafter = screen_2_world(mouse_x, mouse_y)
        world_offset_x += mousebefore[0] - mouseafter[0]
        world_offset_y += mousebefore[1] - mouseafter[1]
        if panning:
            world_offset_x -= (mouse_x - panstart_x) / scale
            world_offset_y -= (mouse_y - panstart_y) / scale
            panstart_x = mouse_x
            panstart_y = mouse_y

            # pos = mouse_2_image(panstart_x, panstart_y, sprite_image_pos[0], sprite_image_pos[1])
            #pos = [(mouse_x - sprite_image_pos[0]), (mouse_y - sprite_image_pos[1])]

            # sprite_image_pos = pos
            # sprite_image_pos = world_2_screen(mouse_x, mouse_y)

            # capture_rect_ex = world_2_screen(capture_rect.x, capture_rect.y)
            # capture_rect.x = capture_rect_ex[0]
            # capture_rect.y = capture_rect_ex[1]
        #

        screen.fill("Black")
        screen.blit(copy_image, sprite_image_pos)

        # Draw capturing rect
        capture_rect_draw()
        # All is done
        pygame.display.update()


main()
