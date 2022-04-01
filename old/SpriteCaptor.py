import pygame
from pygame.locals import *

class SpriteCaptor:
    def __init__(self, thickness=2):
        self.rect = Rect([0, 0, 0, 0])
        self.line_thickness = thickness
        self.scale = 1
        self.font = pygame.font.SysFont('Arial', 25, bold=True)
        self.colors = ["Red", "Black"]
        self.colors_length = len(self.colors) - 1
        self.color = self.colors[1]
        self.color_index = 0
        self.color_max_time = 15
        self.timer = 0
        self.increment = 1
        self.gripping = False
        self.rect_info = self.font.render("x:{}  y:{}  w:{}  h:{}".format(*self.rect), True, "Yellow")

    def reset(self):
        self.rect = Rect([0, 0, 0, 0])

    def update(self, event, image, image_pos):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 3:
                print("SPRITE CAPTOR DOWN")
                if event.pos[0] < 600:
                    self.rect.x, self.rect.y = event.pos
                    self.rect.width = 0
                    self.rect.height = 0
                    self.gripping = True
        elif event.type == MOUSEBUTTONUP:
            if event.button == 3:
                print("SPRITE CAPTOR UP")
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
                self.rect.x -= image_pos[0]
                self.rect.y -= image_pos[1]
                """#capture the whole image if we get nothing
                if not self.capture_sprite(image):
                   self.rect.topleft = (0,0)
                   self.rect.width = image.get_width() - 1
                   self.rect.height = image.get_height() - 1
                   self.capture_sprite(image)"""
                self.capture_sprite(image)
                self.rect.x += image_pos[0]
                self.rect.y += image_pos[1]
                rect_info = self.reset_to_origin(image_pos)
                self.rect_info = self.font.render("x:{}  y:{}  w:{}  h:{}".format(*rect_info), True, "Yellow")
                print(f"INFO IS {self.rect_info}")
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

    def reset_to_origin(self, image_pos):
        x = self.rect.x - image_pos[0]
        y = self.rect.y - image_pos[1]
        x = x / self.scale
        y = y / self.scale
        width = self.rect.width / self.scale
        height = self.rect.height / self.scale
        return Rect([x, y, width, height])

    def scale_rect(self, scale, image_pos):
        self.rect.x -= image_pos[0]
        self.rect.y -= image_pos[1]
        self.rect.x = self.rect.x / self.scale
        self.rect.y = self.rect.y / self.scale
        self.rect.width = self.rect.width / self.scale
        self.rect.height = self.rect.height / self.scale
        self.rect.x = self.rect.x * scale
        self.rect.y = self.rect.y * scale
        self.rect.width = self.rect.width * scale
        self.rect.height = self.rect.height * scale
        self.rect.x += image_pos[0]
        self.rect.y += image_pos[1]
        self.scale = scale

    # Effects ha rectangle/select box
    def cycle_colors(self):
        self.timer += 1
        if self.timer >= self.color_max_time:
            self.timer = 0
            self.color_index += self.increment
            if self.color_index >= self.colors_length:
                self.color_index = self.colors_length
                self.increment *= -1
            elif self.color_index <= 0:
                self.color_index = 0
                self.increment *= -1
            self.color = self.colors[self.color_index]

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, self.line_thickness)
        # Draw Rect Info [ x, y, w ,h]
        pygame.draw.rect(surface, "Black", [0, 400, 250, 35])
        pygame.draw.rect(surface, "White", [0, 400, 250, 35], width=2)
        surface.blit(self.rect_info, (5, 400))

