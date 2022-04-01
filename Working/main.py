import pygame
import sys
import json
from pygame.locals import *
from Working.Util import SpriteCaptor
import ctypes

"""
PANNING/ZOOMING -> WORKING
ADDING BOX IN SPRITE -> WORKING
ZOOMING BOX ALONG WITH SPRITE -> WORKING
ADD BOX SELECTION AROUND SPRITE -> WORKING
PANNING BOX ALONG WITH SPRITE -> WIP / BIG

"""

def get_monitor_size():
    monitor = ctypes.windll.user32
    """Return Monitor Width and Height"""
    return [monitor.GetSystemMetrics(0) - 20, monitor.GetSystemMetrics(1) - 70]


pygame.init()

# Construct WORLD SPACE/SCREEN
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

# - SPRITE CAPTOR -
sprite_captor = SpriteCaptor.SpriteCaptor()
font = pygame.font.SysFont("Arial", 25, bold=True)

# EDITOR VARIABLES
# Image to pan, move around
SPRITESHEET = "assets/M_Swordsman.png"
RIGHT_UI_EDITOR = "assets/sprite_bg.png"
sprite_image = None  # pygame.image.load("assets/M_Swordsman.png").convert()
copy_image = None  # sprite_image.copy()
right_editor_image = None
sprite_image_pos = [0, 0]
ANIMATE = False

# Spritesheet Variables
sprite_list = {}  # Holds all sprites info[x,y,width,height,name,id]
cur_sprite_index = 0  # check what sprite to display based on index
cur_sprite_id = 0  # given id to newly added sprite based on


def save_sprites(data, name):
    """Save current sprites_list in to json format for loading later"""
    f = open(name, "w")
    json.dump(data, f, indent=4)
    f.close()


def load_sprites(name):
    """Load saved sprite data and return its list"""
    try:
        f = open(name, "r")
        data = json.load(f)
        loaded_data = {}
        for d in data:
            rect = data[d]
            loaded_data[int(d)] = rect
        return loaded_data
    except FileNotFoundError:
        print("saved file not found.")
        # Return an empty list
        return {}


def world_2_screen(world_x, world_y):
    """Convert world screen position to screen position"""
    screen_x = int((world_x - world_offset_x) * scale)
    screen_y = int((world_y - world_offset_y) * scale)
    return [screen_x, screen_y]


def screen_2_world(screen_x, screen_y):
    """Convert screen position to world screen position"""
    world_x = int((screen_x / scale) + world_offset_x)
    world_y = int((screen_y / scale) + world_offset_y)
    return [world_x, world_y]


def scale_image(img, _scale):
    """Scale passed image based on specified scale"""
    _width = img.get_width()
    _height = img.get_height()
    #############################################
    # CHECK LATER FOR BUG HERE
    return pygame.transform.scale(img, (_width * _scale, _height * _scale)).convert()


def draw_sprite(s_img, s_rect, s_scale):  # Scaling the sprite selected surface
    """Fetch the sprite at a specified rect and set its alpha color"""
    sprite = s_img.subsurface(s_rect)
    alpha = s_img.get_at((1, 1))
    sprite.set_colorkey(alpha)
    return pygame.transform.scale(s_img, (s_img.get_width() * s_scale, s_img.get_height() * s_scale)).convert_alpha()


def draw_spritecaptor_spritesheet():
    """Draw the spritesheet in the screen along with the sprite captor"""
    global sprite_image_pos
    sprite_image_pos = world_2_screen(0, 0)
    screen.blit(copy_image, sprite_image_pos)
    sprite_captor.draw(screen)


def load_bg_images():
    global sprite_image, right_editor_image
    sprite_image = pygame.image.load(SPRITESHEET).convert_alpha()
    right_editor_image = pygame.image.load(RIGHT_UI_EDITOR).convert_alpha()


def remove_sprite(index):
    """Remove a certain sprite and rebuild the whole list :)"""
    global sprite_list
    cache = sprite_list.copy()
    # remove sprite at specified index
    cache.pop(index)
    # rebuild sprite_list
    c_id = 0
    sprite_list.clear()
    for k in cache.keys():
        sprite_list[c_id] = cache[k]
        c_id += 1


def draw_image_captor():
    """"""
    global sprite_image_pos, copy_image, sprite_image_pos, sprite_captor
    # Draw captor
    sprite_image_pos = world_2_screen(0, 0)
    screen.blit(copy_image, sprite_image_pos)
    sprite_captor.draw(screen)


def handle_saving():
    save_sprites(sprite_list, "sheet_1.json")
    print("Sprite sheet saved.")


def handle_input(event):
    global cur_sprite_index, cur_sprite_id, ANIMATE
    if event.type == KEYDOWN:
        if event.key == K_e:
            cur_sprite_index += 1
            if cur_sprite_index > len(sprite_list) - 1:
                cur_sprite_index = 0
        elif event.key == K_q:
            cur_sprite_index -= 1
            if cur_sprite_index < 0:
                cur_sprite_index = len(sprite_list) - 1
        elif event.key == K_SPACE:
            # Add new selected sprite to sprites_list
            x, y, w, h = sprite_captor.reset_to_origin(sprite_image_pos)
            if [x, y, w, h] != [0, 0, 0, 0]:
                # update sprite ID to match count
                sprite_data = {"sname": 0, "srect": [x, y, w, h], "saxis": [-int(w / 2), -h]}
                sprite_list[cur_sprite_id] = sprite_data
                print("SPRITE ADDED : {}".format((x, y, w, h)))
                cur_sprite_id += 1
                cur_sprite_index = cur_sprite_id - 1
            else:
                print("EMPTY RECT")
        elif event.key == K_ESCAPE:
            handle_saving()
            #
        elif event.key == K_DELETE:  # Remove current viewing sprite
            if len(sprite_list) > 0:
                # is current index in the beginning or the last index
                if cur_sprite_index == 0:
                    remove_sprite(cur_sprite_index)
                    cur_sprite_index = 0
                    cur_sprite_id -= 1
                elif cur_sprite_index == len(sprite_list) - 1 or cur_sprite_index < len(sprite_list) - 1:
                    remove_sprite(cur_sprite_index)
                    cur_sprite_index -= 1
                    cur_sprite_id -= 1
        elif event.key == K_p:
            ANIMATE = not ANIMATE


def drawCurSprite(cur_screen, sprites, sprite_sheet, sprite_axis=None,
                  sprite_scale=2):
    if sprite_axis is None:
        sprite_axis = [SCREEN_WIDTH - (right_editor_image.get_width() / 2), 180]
    s_rect = Rect(sprites['srect'])
    s_axis = sprites['saxis']
    axis_pos = sprite_axis  # Change this later for the final position of Sprite Window
    s_pos = [s_axis[0] * sprite_scale + axis_pos[0], s_axis[1] * sprite_scale + axis_pos[1]]
    # sprite = scale_image(image, _scale)
    sprite = sprite_sheet.subsurface(s_rect)
    alpha = sprite_sheet.get_at((1, 1))
    sprite = pygame.transform.scale(sprite, (sprite.get_width() * sprite_scale,
                                             sprite.get_height() * sprite_scale)).convert()
    sprite.set_colorkey(alpha)
    cur_screen.blit(sprite, s_pos)


def main():
    # Initialize some functions
    global sprite_list, cur_sprite_index, cur_sprite_id, copy_image, \
        panstart_x, panstart_y, panning, sprite_image_pos, \
        zoomin, zoomout, scale, world_offset_x, world_offset_y

    pygame.key.set_repeat(500, 100)

    load_bg_images()
    copy_image = sprite_image.copy()
    sprite_list = load_sprites("sheet_1.json")

    if len(sprite_list) > 0:
        cur_sprite_index = 0
        cur_sprite_id = len(sprite_list)
    else:
        print("JSON FILE NOT FOUND")

    running = True

    framerate = 0
    while running:
        clock.tick(fps)
        events = pygame.event.get()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # AUTOMATIC PLAYBACK ALL SPRITES
        if ANIMATE:
            if framerate > 8:
                cur_sprite_index += 1
                if cur_sprite_index > len(sprite_list) - 1:
                    cur_sprite_index = 0
                framerate = 0
            framerate += 1

        # FOR START
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # panning and zooming of mouse
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

            # Inputs
            handle_input(event)
            # Process sprite_captor's update
            sprite_captor.update(event, copy_image, sprite_image_pos)
        # Refresh captor selection box
        sprite_captor.cycle_colors()

        # -- ZOOMING PORTION --
        mousebefore = screen_2_world(mouse_x, mouse_y)
        if zoomin and scale < 4:
            scale += 1
            zoomin = False
            copy_image = scale_image(sprite_image, scale)
            sprite_captor.scale_rect2(scale, sprite_image_pos)
            # Reset captor rect
            # Dire ko pa na aayad an kun ma zoom ako hn sprite an size
            # and position hn captor is ma adjust based hn scale
            # so yana reset la anay an rect
            sprite_captor.reset()
        if zoomout and scale > 1:
            scale -= 1
            zoomout = False
            # Scale viewing sprite
            copy_image = scale_image(sprite_image, scale)
            sprite_captor.scale_rect2(scale, sprite_image_pos)
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

        # -- PANNING PORTION --
        mouseafter = [mouse_x, mouse_y]
        new_x = panstart_x - mouseafter[0]
        new_y = panstart_y - mouseafter[1]

        if panning:
            world_offset_x -= (mouse_x - panstart_x) / scale
            world_offset_y -= (mouse_y - panstart_y) / scale
            panstart_x = mouse_x
            panstart_y = mouse_y
            # print("Panning")
            sprite_captor.rect.x -= new_x
            sprite_captor.rect.y -= new_y


        # Draw Everything
        screen.fill("Black")
        # Draw sprite captor along with the spritesheet
        draw_image_captor()
        # Draw right editor
        screen.blit(right_editor_image, (SCREEN_WIDTH - right_editor_image.get_width(), 0, 200, 500))
        pygame.draw.rect(screen, "White", (SCREEN_WIDTH - right_editor_image.get_width(), 0, 200, 500), width=2)

        # current sprite
        if len(sprite_list) > 0:
            drawCurSprite(screen, sprite_list[cur_sprite_index], sprite_image)

        pygame.display.update()


if __name__ == "__main__":
    main()
