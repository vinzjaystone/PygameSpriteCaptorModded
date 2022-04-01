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

def capture_rect_detail(copy):
    global capture_rect, sprite_image
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


def scale_image(image, image_scale):
    # CHECK LATER FOR BUG HERE
    return pygame.transform.scale(image, (image.get_width() * image_scale,
                                          image.get_height() * image_scale)).convert()


boxes = []

def add_box(rect):
    boxes.append(rect)

# TODO: 1
# REGARDLESS HT CURRENT SCALE
# KUN NAG DRAW AKO HN BOX HA SCALE 2
# DAPAT IG IYA SIZE DIRE MA x2 DAUN
# KUN MAG ZOOMOUT AKO MA GUTI IYA
# BUG FIXED/DONE
def draw_boxes():
    for b in boxes:
        x, y, w, h = b[0], b[1], b[2], b[3]
        pos = world_2_screen(x, y)
        rect = Rect([pos[0], pos[1], w * scale, h * scale])
        pygame.draw.rect(screen, "Yellow", rect, 3)


def pre_draw(p1, p2):
    # Draw
    # get first pos
    # get current second pos
    # get current width, height
    _h = p2[1] - p1[1]
    _w = p2[0] - p1[0]
    # p1 = screen_2_world(p1[0], p1[1])
    r = Rect([p1[0], p1[1], _w, _h])
    pygame.draw.rect(screen, "Yellow", r)


def draw_image():
    pass


def capture_sprite(self, image):
    try:
        capturing_rect = Rect([0, 0, 0, 0])
        alpha_color = image.get_at(self.rect.topleft)
        other_color = False

        old_x = self.rect.x + self.rect.width
        for y in range(self.rect.y, self.rect.y + self.rect.height, 1):
            for x in range(self.rect.x, self.rect.x + self.rect.width, 1):
                if image.get_at((x, y)) != alpha_color:
                    other_color = True
                    if x < old_x:
                        old_x = x
                        capturing_rect.x = x
                        break
        if other_color:
            old_x = self.rect.x
            for y in range(self.rect.y, self.rect.y + self.rect.height, 1):
                for x in range(self.rect.x + self.rect.width, self.rect.x - 1, -1):
                    if image.get_at((x, y)) != alpha_color:
                        if x > old_x:
                            old_x = x
                            if x > self.rect.x:
                                capturing_rect.width = (x + 1) - capturing_rect.x
                            break

            old_y = self.rect.y + self.rect.height
            for x in range(self.rect.x, self.rect.x + self.rect.width, 1):
                for y in range(self.rect.y, self.rect.y + self.rect.height, 1):
                    if image.get_at((x, y)) != alpha_color:
                        if y < old_y:
                            old_y = y
                            capturing_rect.y = y
                            break

            old_y = self.rect.y
            for x in range(self.rect.x, self.rect.x + self.rect.width, 1):
                for y in range(self.rect.y + self.rect.height, self.rect.y - 1, -1):
                    if image.get_at((x, y)) != alpha_color:
                        if y > old_y:
                            old_y = y
                            if y > self.rect.y:
                                capturing_rect.height = (y + 1) - capturing_rect.y
                            break

            self.rect = capturing_rect
        # return other_color
    except IndexError:
        # Cancel capture
        # out of bound pixel detected
        pass


def main():
    global panning, panstart_x, panstart_y, scale, world_offset_x, world_offset_y, zoomin, zoomout
    global sprite_image, sprite_image_pos, copy_image

    global capture_gripping, capture_rect


    # Load spritesheet


    running = True
    gripping = False
    box_rect_x = 0
    box_rect_y = 0
    # box_rect_w = 0
    # box_rect_h = 0

    firstRectPos = [0, 0]
    secondRectPos = [0, 0]
    hasFirstRect = False

    # Test capture rect of image
    capturing_rect = Rect([0, 0, 0, 0])

    while running:
        clock.tick(fps)
        events = pygame.event.get()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # FOR START
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 3 and gripping is False:
                    if event.pos[0] < 600:
                        capture_rect.x, capture_rect.y = event.pos
                        capture_rect.width = 0
                        capture_rect.height = 0
                        capture_gripping = True

                    box_rect_x = event.pos[0]
                    box_rect_y = event.pos[1]
                    #
                    firstRectPos = [mouse_x, mouse_y]
                    hasFirstRect = True

                    gripping = True
                elif event.button == 1:
                    panstart_x = mouse_x
                    panstart_y = mouse_y
                    panning = True
                elif event.button == 4 or event.button == 5:
                    if event.button == 4 and scale < scale_max:
                        zoomin = True
                    elif event.button == 5 and scale > 1:
                        zoomout = True
            elif event.type == MOUSEBUTTONUP:
                if event.button == 3 and gripping is True:
                    #
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

                    boxes.append(capture_rect)
                    #

                    capture_rect = Rect([0, 0, 0, 0])







                    box_rect_w = event.pos[0] - box_rect_x
                    box_rect_h = event.pos[1] - box_rect_y
                    box_rect = screen_2_world(box_rect_x, box_rect_y)
                    # divide width and height based on the level of current scale
                    # so that when i scale at Level 2, the width/height should be divided
                    # by too also so when i return to level 1 it will change correspondingly
                    # boxes.append([box_rect[0], box_rect[1], box_rect_w / scale, box_rect_h / scale])




                    # boxes.append([box_rect[0], box_rect[1], box_rect_w / scale, box_rect_h / scale])
                    box_rect_x = 0
                    box_rect_y = 0

                    # ---------------------- #
                    # PRE DRAW
                    firstRectPos = [0, 0]
                    secondRectPos = [0, 0]
                    hasFirstRect = False
                    # ---------------------- #

                    gripping = False
                elif event.button == 1:
                    panning = False

                    # box_rect = screen_2_world()
                    # boxes.append([box_rect_x, box_rect_y])
                    # boxes.append([box_rect_x, box_rect_y, box_rect_w, box_rect_h])
            elif event.type == MOUSEMOTION:
                if capture_gripping:
                    # CHECK LATER DINHE KUN MYDA ERROR HA SCALING
                    capture_rect.width = event.pos[0] - capture_rect.x
                    capture_rect.height = event.pos[1] - capture_rect.y
        mousebefore = screen_2_world(mouse_x, mouse_y)

        # -------------------------------------- #
        # FOR PRE DRAW SELECTION RECT
        if hasFirstRect is True:
            secondRectPos = [mouse_x, mouse_y]
        # -------------------------------------- #

        if zoomin and scale < scale_max:
            scale += 1
            # Added November 9
            copy_image = scale_image(sprite_image, scale)
            #
            zoomin = False
        if zoomout and scale > 1.0:
            scale -= 1
            # Added November 9
            copy_image = scale_image(sprite_image, scale)
            #
            zoomout = False
        mouseafter = screen_2_world(mouse_x, mouse_y)
        world_offset_x += mousebefore[0] - mouseafter[0]
        world_offset_y += mousebefore[1] - mouseafter[1]
        if panning:
            world_offset_x -= (mouse_x - panstart_x) / scale
            world_offset_y -= (mouse_y - panstart_y) / scale
            panstart_x = mouse_x
            panstart_y = mouse_y

        screen.fill("Black")
        # sprite_image_pos = world_2_screen(0, 0)
        screen.blit(copy_image, sprite_image_pos)
        draw_boxes()

        # TODO: 2
        # Pre Draw selection rect
        if firstRectPos != [0, 0] or secondRectPos != [0, 0]:
            pre_draw(firstRectPos, secondRectPos)
            # print("Drawing")



        pygame.display.update()
    # pass


if __name__ == "__main__":
    main()
