import pygame

SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
surface = screen

# item effect -------------------------------------------------------------------------------

def healplayer(player, value):
    player.health += value


# ------------------------------------------------------------------------------------
class Chest():
    def __init__(self, name, x, y, flip, data, sprite_sheet, animation_steps, sound, item):
        self.name = name
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = False
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0  # 0close 1open
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 32, 22))
        self.active = True
        self.open = False
        self.opensound = sound
        self.item = item

    def load_images(self, sprite_sheet, animation_steps):
        # extract images from spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def update(self, player):
        # check what action the player is performing
        if self.active == True:
            if self.open == False:
                self.update_action(0)  # 0close
            elif self.open == True:
                self.image = self.animation_list[0][1]
                # self.opensound.play()

        if player.interact == True and player.rect.x >= 520 and player.rect.x < 770:
            self.open = True

    def dropitem(self, item):
        pass

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


class Item():
    def __init__(self, x, y, image, scale, effect):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), (int(height * scale))))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel_y = 0
        self.jump = False
        self.jumpcooldown = 0
        self.jumpcheck = 1
        self.active = True
        self.use = 1
        self.moving = True
        self.effect = effect

    def draw(self):
        if self.active == True:
            screen.blit(self.image, (self.rect.x, self.rect.y))
            # debug pygame.draw.rect(surface, (0, 0, 255), self.rect, 2)

    def update(self, player):
        self.player = player
        if self.rect.y != 594:
            self.moving = True
        else:
            self.moving = False
        if self.player.interact == True and self.player.rect.colliderect(self.rect) and self.use == 1 and self.moving == False:
            self.effect(player, 50)
            self.use = 0
            self.active = False

    def gravity(self):
        GRAVITY = 1
        dx = 0
        dy = 0
        self.jump = True
        screen_width = SCREEN_WIDTH
        screen_height = SCREEN_HEIGHT
        # apply gravity
        if self.jumpcheck == 1 and self.jumpcooldown == 0:
            self.vel_y = -20
            self.jumpcheck = 0

        self.vel_y += GRAVITY
        dy += self.vel_y

        # ensure player stays on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 62 - self.rect.bottom

        # update player position
        self.rect.x += dx
        self.rect.y += dy
        print(self.rect.y)