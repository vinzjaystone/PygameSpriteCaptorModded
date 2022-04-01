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
world_offset_x, world_offset_y = 0, 0
panstart_x, panstart_y = 0, 0
scale = 1
zoomin = False
zoomout = False
panning = False

SPRITESHEET = "assets/copy.png"
sprite_image = pygame.image.load(SPRITESHEET).convert_alpha()
copy_image = sprite_image.copy()
sprite_image_pos = [0, 0]


def world_2_screen(world_x, world_y):
    """Convert world screen position to screen position"""
    screen_x = int((world_x - world_offset_x) * scale)
    screen_y = int((world_y - world_offset_y) * scale)
    return [screen_x, screen_y]


def offset_2_screen(p_x, p_y, off_x, off_y):
    return [(p_x + off_x), (p_y + off_y)]


def screen_2_world(screen_x, screen_y):
    """Convert screen position to world screen position"""
    world_x = int((screen_x / scale) + world_offset_x)
    world_y = int((screen_y / scale) + world_offset_y)
    return [world_x, world_y]

class SpriteCaptorMini:
    def __init__(self):
        self.rect = Rect([0, 0, 0, 0])
        self.orig_rect = Rect([0, 0, 0, 0])
        self.rect_changed = False
        self.scale = 1
        self.gripping = False
        pass

    # Get mouse position
    # set rect.x,y
    # monitor mouse motion
    # update rect.width and height
    # based on new mouse position

    def update(self, event, image, image_pos):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 3:
                if event.pos[0] < 600:
                    self.rect.x, self.rect.y = event.pos
                    self.rect.width = 0
                    self.rect.height = 0
                    self.gripping = True
        elif event.type == MOUSEBUTTONUP:
            if event.button == 3:
                self.gripping = False
                if self.rect.width < 0:
                    self.rect.width *= -1
                    self.rect.x -= self.rect.width
                if self.rect.height < 0:
                    self.rect.height *= -1
                    self.rect.y -= self.rect.height
                image_rect = image.get_rect()
                image_rect.topleft = image_pos
                # check for overflow
                if self.rect.right > image_rect.right \
                        or self.rect.left < image_rect.left \
                        or self.rect.bottom > image_rect.bottom \
                        or self.rect.top < image_rect.top:
                    self.rect.topleft = image_rect.topleft
                    self.rect.size = (0, 0)
                    #  Na rereset it rect dinhe kun it selection rect is gawas hit image
                self.rect.x -= image_pos[0]
                self.rect.y -= image_pos[1]

                """#capture the whole image if we get nothing
                if not self.capture_sprite(image):
                   self.rect.topleft = (0,0)
                   self.rect.width = image.get_width() - 1
                   self.rect.height = image.get_height() - 1
                   self.capture_sprite(image)"""
                self.capture_sprite(image)
                # self.rect.x += image_pos[0]
               # self.rect.y += image_pos[1]
        if event.type == MOUSEMOTION:
            if self.gripping:
                self.rect.width = event.pos[0] - self.rect.x
                self.rect.height = event.pos[1] - self.rect.y


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


    def draw_rect(self, surface):
        pygame.draw.rect(surface, "Red", self.rect, 4)

    def scale_rect(self, s_scale, image_pos, copy_img):
        # divide by previous scale
        self.rect.width = self.rect.width / self.scale
        self.rect.height = self.rect.height / self.scale
        # multiply by new scale
        w = self.rect.width = self.rect.width * s_scale
        h = self.rect.height = self.rect.height * s_scale
        # Set previous scale to new scale
        self.scale = s_scale
        print(image_pos)


        # w, h = self.rect.width / self.scale, self.rect.height / self.scale
        # w =
        # self.rect.x = +image_pos[0]
        # self.rect.y = +image_pos[1]


        # pos = screen_2_world(-self.rect.x, -self.rect.y)
        # self.rect.x = -pos[0]
        # self.rect.y = -pos[1]

        # get current rect width and height
        # get copy_image width and heigh

        # print(f"Image Size {} {}")

        #self.rect.x -= image_pos[0]
        #self.rect.y -= image_pos[1]
        #self.rect.x = self.rect.x / self.scale
        #self.rect.y = self.rect.y / self.scale
        #self.rect.x = self.rect.x * scale
        #self.rect.y = self.rect.y * scale
        #self.rect.x += image_pos[0]
        #self.rect.y += image_pos[1]


def scale_image(img, img_scale):
    """Scale passed image based on specified scale"""
    #############################################
    # CHECK LATER FOR BUG HERE
    return pygame.transform.scale(img, (img.get_width() * img_scale,
                                        img.get_height() * img_scale)).convert()

def show(x, y, txt):
    print(f"{txt} - X : {x}   Y : {y}")

def main():
    global panstart_x, panstart_y, panning, sprite_image_pos, \
        zoomin, zoomout, scale, world_offset_x, world_offset_y, copy_image
    pygame.key.set_repeat(500, 100)

    sprite_captor = SpriteCaptorMini()
    # captor_rect = Rect([0, 0, 0, 0])

    running = True
    debug_timer = 0
    while running:
        clock.tick(fps)
        events = pygame.event.get()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        debug_timer += 1

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
                # for mouse wheel
                elif event.button == 4 or event.button == 5:
                    if event.button == 4 and scale < 4:
                        zoomin = True
                    elif event.button == 5 and scale > 1:
                        zoomout = True
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1 and panning is True:
                    panning = False
            # Add spritecaptor update
            sprite_captor.update(event, sprite_image, sprite_image_pos)

        # -- ZOOMING PORTION --
        mousebefore = screen_2_world(mouse_x, mouse_y)
        if zoomin and scale < 4:
            scale += 1
            print(f"Before Width : {copy_image.get_width()}")
            copy_image = scale_image(sprite_image, scale)
            # print(f"Copy Image : {copy_image.get_rect()}")
            print(f"After Width : {copy_image.get_width()}")
            sprite_captor.scale_rect(scale, sprite_image_pos, copy_image)

            zoomin = False
            # Reset captor rect
            # Dire ko pa na aayad an kun ma zoom ako hn sprite an size
            # and position hn captor is ma adjust based hn scale
            # so yana reset la anay an rect
            # sprite_captor.reset()
        if zoomout and scale > 1:
            scale -= 1
            # Scale viewing sprite
            print(f"Before Width : {copy_image.get_width()}")
            copy_image = scale_image(sprite_image, scale)
            print(f"Copy Image : {copy_image.get_rect()}")
            print(f"After Width : {copy_image.get_width()}")
            sprite_captor.scale_rect(scale, sprite_image_pos, copy_image)
            zoomout = False
            # Reset captor rect
            # Dire ko pa na aayad an kun ma zoom ako hn sprite an size
            # and position hn captor is ma adjust based hn scale
            # so yana reset la anay an rect
            # sprite_captor.reset()


        mouseafter = screen_2_world(mouse_x, mouse_y)

        world_offset_x += (mousebefore[0] - mouseafter[0])
        world_offset_y += (mousebefore[1] - mouseafter[1])
        # -- END ZOOMING --

        # For moving the captor rect
        mousea = [mouse_x, mouse_y]
        new_x = panstart_x - mousea[0]
        new_y = panstart_y - mousea[1]

        # sprite_captor.scale_rect(scale, sprite_image_pos, copy_image)
        if panning:
            # print(f"Pos Image : {sprite_image_pos}")
            world_offset_x -= (mouse_x - panstart_x) / scale
            world_offset_y -= (mouse_y - panstart_y) / scale
            panstart_x = mouse_x
            panstart_y = mouse_y


            sprite_captor.rect.x -= new_x
            sprite_captor.rect.y -= new_y
            #
            # pos_a = screen_2_world(sprite_captor.rect.x, sprite_captor.rect.y)
            # pos_b = world_2_screen(0, 0)
            #
            # # captor_rect = screen_2_world(captor_rect[0], captor_rect[1])
            # sprite_captor.rect.x = -captor_rect[0]
            # sprite_captor.rect.y = -captor_rect[1]

            # if debug_timer >= 20:
            #     show(world_offset_x, world_offset_y, "Offset")
            #     #print(f"Offset X : {world_offset_x}   Offset Y {world_offset_y}")
            #     debug_timer = 0

            #


        screen.fill("Black")

        sprite_image_pos = world_2_screen(0, 0)
        screen.blit(copy_image, sprite_image_pos)

        sprite_captor.draw_rect(screen)
        pygame.display.update()


if __name__ == "__main__":
    main()
