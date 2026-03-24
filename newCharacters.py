import pygame
import random


class Character():
    def __init__(self, name, x, y, flip, data, sprite_sheet, animation_steps, sound, statimg):
        self.name = name
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = False
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0  # 0:idle 1:run 2:jump 3:attack1 4:attack2 5:hit 6:death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound = sound
        self.hit = False
        self.health = 100
        self.mana = 100
        self.alive = True
        self.attackindex = 1
        self.jumpcooldown = 0
        self.interact = False
        self.xloc = x
        self.attacking_rect = pygame.Rect(self.rect.centerx - (6 * self.rect.width * self.flip), self.rect.y, 6 * self.rect.width, self.rect.height)
        self.statimg = statimg
        if self.name == "p1":
            self.damage = 15
        if self.name == "p2":
            self.damage = 15

    # Spritesheet Loader
    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        # Player Controls
        key = pygame.key.get_pressed()

        if self.alive == True and round_over == False:
            if self.name == "p1":
                SPEED = 15
            elif self.name == "p2":
                SPEED = 9

            # movement
            if key[pygame.K_a]:
                dx = -SPEED
                self.running = True
                self.flip = True
            if key[pygame.K_d]:
                dx = SPEED
                self.running = True
                self.flip = False
            # jump
            if key[pygame.K_w] and self.jump == False and self.jumpcooldown == 0:
                self.vel_y = -30
                self.jump = True
                self.mana -= 5

            # attack
            if self.name == "p1":
                if key[pygame.K_p]:
                    if key[pygame.K_p] and self.attackindex == 1 and self.attack_cooldown == 0:
                        self.attack(target)
                        self.attack_type = 1
                        self.attack_cooldown = 45   # 0.75 seconds at 60 FPS
                    if key[pygame.K_p] and self.attackindex == 2 and self.attack_cooldown == 0:
                        self.attack(target)
                        self.attack_type = 2
                        self.attack_cooldown = 45   # 0.75 seconds at 60 FPS
                if self.action == 3 and self.frame_index >= 5:
                    self.attackindex = 2
                elif self.action == 4 and self.frame_index >= 5:
                    self.attackindex = 1

            elif self.name == "p2":
                if key[pygame.K_p]:
                    if key[pygame.K_p]:
                        if key[pygame.K_p] and not self.jump:
                            self.attack(target)
                            self.attack_type = 1
                            self.attack_cooldown = 45   # 0.75 seconds at 60 FPS
                        if key[pygame.K_p] and self.jump:
                            self.jumpattack(target)
                            self.attack_type = 2
                            self.attack_cooldown = 45   # 0.75 seconds at 60 FPS

            if key[pygame.K_a] or key[pygame.K_d]:
                if key[pygame.K_LSHIFT]:
                    if self.flip == True and self.mana > 10:
                        dx -= 20
                        self.mana -= 2
                    elif self.flip == False:
                        dx += 20
                        self.mana -= 2

            if key[pygame.K_e]:
                self.interact = True
            elif self.interact == True:
                self.interact = False

        # apply gravity
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
            dy = screen_height - 110 - self.rect.bottom

        # apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if self.jumpcooldown > 0:
            self.jumpcooldown -= 1

        # update player position
        self.rect.x += dx
        self.rect.y += dy

    # handle animation updates
    def update(self):
        if self.health > 100:
            self.health = 100
        if self.mana < 99.9:
            self.mana += .5
        if self.mana < 0:
            self.mana = 0
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)  # 6:death
        elif self.hit == True:
            self.update_action(5)  # 5:hit
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)  # 3:attack1
            elif self.attack_type == 2:
                self.update_action(4)  # 4:attack2
        elif self.jump == True:
            self.update_action(2)  # 2:jump
            self.jumpcooldown = 15
        elif self.running == True:
            self.update_action(1)  # 1:run
        else:
            self.update_action(0)  # 0:idle

        animation_cooldown = 50

        self.image = self.animation_list[self.action][self.frame_index]

        if self.attacking and self.frame_index == 0 and self.attack_cooldown == 0:
            self.attack_sound.play()

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.animation_list[self.action]):
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 45   # 0.75 seconds at 60 FPS
                if self.action == 5:
                    self.hit = False
                    self.attacking = False
                    self.attack_cooldown = 45   # 0.75 seconds at 60 FPS

    def attack(self, target):
        if self.attack_cooldown == 0 and self.mana > 20:
            self.mana -= 15
            self.attacking = True
            self.attack_sound.play()
            if self.name == "p1":
                self.attacking_rect = pygame.Rect(self.rect.centerx - (6 * self.rect.width * self.flip), self.rect.y, 6 * self.rect.width, self.rect.height)
            elif self.name == "p2":
                self.attacking_rect = pygame.Rect(self.rect.centerx - (3.5 * self.rect.width * self.flip), self.rect.y, 3.5 * self.rect.width, self.rect.height)
            if self.attacking_rect.colliderect(target.rect):
                # ── Worm immunity: melee attacks deal 0 damage ──────────────
                if not getattr(target, 'melee_immune', False):
                    target.health -= self.damage
                    print("Enemy HP " + str(target.health))
                    target.hit = True
                else:
                    print("Worm is immune to melee attacks!")

    def jumpattack(self, target):
        if self.attack_cooldown == 0 and self.mana > 20:
            self.mana -= 15
            self.attacking = True
            self.attack_sound.play()
            self.attacking_rect = pygame.Rect(self.rect.centerx - 300, self.rect.y + 100, 6 * self.rect.width, self.rect.height)
            if self.attacking_rect.colliderect(target.rect):
                # ── Worm immunity: jump melee attacks also deal 0 damage ────
                if not getattr(target, 'melee_immune', False):
                    target.health -= self.damage
                    print("Enemy HP " + str(target.health))
                    target.hit = True
                else:
                    print("Worm is immune to melee attacks!")

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))


    # ------------------------------------------------------------------------debug
    '''
    def draw_character_rect(self, surface):
            pygame.draw.rect(surface, (0, 0, 255), self.rect, 2)

    def draw_attacking_rect(self, surface):
            if self.jump:
                if self.name == "p2":
                    self.attacking_rect = pygame.Rect(self.rect.centerx - 300,
                                                 self.rect.y+100, 6 * self.rect.width, self.rect.height)
                    pygame.draw.rect(surface, (255, 0, 0), self.attacking_rect, 2)
            elif self.jump == False:
                if self.name == "p1":
                    self.attacking_rect = pygame.Rect(self.rect.centerx - (6 * self.rect.width * self.flip),
                                                 self.rect.y, 6 * self.rect.width, self.rect.height)
                elif self.name == "p2":
                    self.attacking_rect = pygame.Rect(self.rect.centerx - (3.5 * self.rect.width * self.flip),
                                                 self.rect.y, 3.5 * self.rect.width, self.rect.height)
                pygame.draw.rect(surface, (255, 0, 0), self.attacking_rect, 2)'''
    # ------------------------------------------------------------------------debug


# function for drawing fighter health bar
def draw_health_bar(health, x, y):
    ratio = health / 100


# function for drawing fighter mana bar
def draw_mana_bar(mana, x, y):
    ratio = mana / 100


# function for drawing goblin health bar
def draw_health_gob(health, x, y):
    ratio = health / 100


class Player(Character):
    def __init__(self, level, experience):
        super().__init__(self, level, experience)

        @classmethod
        def level_up(self, player):
            self.player = player


class Monster_humanoid(Character):
    def __init__(self, name, x, y, flip, data, sprite_sheet, animation_steps, sound, statimg):
        super().__init__(name, x, y, flip, data, sprite_sheet, animation_steps, sound, statimg)
        self.name = name
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = True
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0  # 0:idle 1:run 2:jump 3:attack1 4:attack2 5:hit 6:death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound = sound
        self.hit = False
        self.health = 100
        self.mana = 100
        self.alive = True
        self.attackindex = 1
        self.jumpcooldown = 0
        self.interact = False
        self.damage = 25
        self.damagetoken = 1

    def move(self, screen_width, screen_height, surface, target, round_over, xpos):
        SPEED = 6
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0
        self.xpos = xpos

        if self.alive == True and self.attacking == False and round_over == False and self.rect.x - 200 >= self.xpos:
            dx = -SPEED
            self.running = True
            self.flip = True
            if self.attack_cooldown != 0:
                dx = SPEED

        if self.rect.x - self.xpos < 300 and self.attack_cooldown == 0 and self.flip == True:
            self.attack(target)
            self.attack_type = 1

        if self.alive == True and round_over == False and self.attacking == False and self.rect.x + 200 <= self.xpos:
            dx = SPEED
            self.running = True
            self.flip = False
            if self.attack_cooldown != 0:
                dx = -SPEED

        if self.rect.x - self.xpos > -300 and self.attack_cooldown == 0 and self.flip == False:
            self.attack(target)
            self.attack_type = 1

        # apply attack cooldown (frame-based, decrement by 1 per frame)
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # knockback
        if self.flip and self.hit and self.alive:
            dx = 2
        if self.flip == False and self.hit and self.alive:
            dx = -2

        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom

        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        if self.health > 100:
            self.health = 100
        if self.mana < 99.9:
            self.mana += 40
        if self.mana < 0:
            self.mana = 0
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)  # 6:death
        elif self.hit == True:
            self.update_action(5)  # 5:hit
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)  # 3:attack1
            elif self.attack_type == 2:
                self.update_action(4)  # 4:attack2
        elif self.jump == True:
            self.update_action(2)  # 2:jump
            self.jumpcooldown = 15
        elif self.running == True:
            self.update_action(1)  # 1:run
        else:
            self.update_action(0)  # 0:idle

        animation_cooldown = 50

        self.image = self.animation_list[self.action][self.frame_index]

        if self.attacking and self.frame_index == 0 and self.attack_cooldown == 0:
            self.attack_sound.play()

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.animation_list[self.action]):
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 45   # 0.75 seconds at 60 FPS
                if self.action == 5:
                    self.hit = False
                    self.attacking = False
                    self.attack_cooldown = 45   # 0.75 seconds at 60 FPS

    def attack(self, target):
        self.attacking_rect = pygame.Rect(self.rect.centerx - (4 * self.rect.width * self.flip),
                                          self.rect.y * 1, 4 * self.rect.width, self.rect.height * .5)

        if self.attack_cooldown == 0 and self.alive == True and target.health > 0 and self.attacking == False:
            self.attacking = True
            self.attack_sound.play()

        if self.attacking == True:
            hit = self.attacking_rect.colliderect(target.rect)
            if hit == True and self.frame_index == 6 and self.damagetoken == 1:
                self.damagetoken = 0
                target.health -= self.damage
                target.hit = False
            elif self.damagetoken == 0:
                self.damagetoken = 1


# Goblin AI
class Monster(Character):
    def __init__(self, name, x, y, flip, data, sprite_sheet, animation_steps, sound, statimg):
        super().__init__(name, x, y, flip, data, sprite_sheet, animation_steps, sound, statimg)
        self.flip = True
        self.alive = True
        self.damagetoken = 1

    def move(self, screen_width, screen_height, surface, target, round_over, xpos):
        SPEED = 6
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0
        self.xpos = xpos
        self.damage = 7

        if self.alive == True and self.attacking == False and round_over == False and self.rect.x - 200 >= self.xpos:
            dx = -SPEED
            self.running = True
            self.flip = True

        if self.rect.x - self.xpos < 300 and self.attack_cooldown == 0 and self.flip == True:
            self.attack(target)
            self.attack_type = 1

        if self.alive == True and round_over == False and self.attacking == False and self.rect.x + 200 <= self.xpos:
            dx = SPEED
            self.running = True
            self.flip = False

        if self.rect.x - self.xpos > -300 and self.attack_cooldown == 0 and self.flip == False:
            self.attack(target)
            self.attack_type = 1

        # apply attack cooldown (frame-based, decrement by 1 per frame)
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # knockback
        if self.flip and self.hit and self.alive:
            dx = 2
        if self.flip == False and self.hit and self.alive:
            dx = -2

        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(1)
        elif self.hit == True:
            self.update_action(4)
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(0)
            elif self.attack_type == 2:
                self.update_action(0)
        elif self.running == True:
            self.update_action(3)
        else:
            self.update_action(2)

        animation_cooldown = 50

        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.animation_list[self.action]):
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                if self.action == 0:
                    self.attacking = False
                    self.attack_cooldown = 45   # 0.75 seconds at 60 FPS
                if self.action == 4:
                    self.hit = False
                    self.attacking = False
                    self.attack_cooldown = 45   # 0.75 seconds at 60 FPS

    def attack(self, target):
        self.attacking_rect = pygame.Rect(self.rect.centerx - (3 * self.rect.width * self.flip),
                                          self.rect.y * 1.15, 3 * self.rect.width, self.rect.height * .5)

        if self.attack_cooldown == 0 and self.alive == True and target.health > 0 and self.attacking == False:
            self.attacking = True
            self.attack_sound.play()

        if self.attacking == True:
            hit = self.attacking_rect.colliderect(target.rect)
            if hit == True and self.frame_index == 6 and self.damagetoken == 1:
                self.damagetoken = 0
                target.health -= self.damage
                print("Main MC HP " + str(target.health))
                target.hit = False
            elif self.damagetoken == 0:
                self.damagetoken = 1


class Monster_Skeleton(Monster):
    def __init__(self, name, x, y, flip, data, sprite_sheet, animation_steps, sound, statimg):
        super().__init__(name, x, y, flip, data, sprite_sheet, animation_steps, sound, statimg)
        self.flip = True
        self.alive = True
        self.damagetoken = 1
        self.truehit = False
        self.falsehit = False
        self.regenrate = .013

    def move(self, screen_width, screen_height, surface, target, round_over, xpos):
        SPEED = 4   # Increased from 2
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0
        self.xpos = xpos
        self.damage = 6   # Increased from 3

        if self.alive == True and self.attacking == False and round_over == False and self.rect.x - 200 >= self.xpos:
            dx = -SPEED
            self.running = True
            self.flip = True

        if self.rect.x - self.xpos < 300 and self.attack_cooldown == 0 and self.flip == True:
            self.attack(target)
            self.attack_type = 1

        if self.alive == True and round_over == False and self.attacking == False and self.rect.x + 200 <= self.xpos:
            dx = SPEED
            self.running = True
            self.flip = False

        if self.rect.x - self.xpos > -300 and self.attack_cooldown == 0 and self.flip == False:
            self.attack(target)
            self.attack_type = 1

        # apply attack cooldown (frame-based, decrement by 1 per frame)
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # knockback
        if self.flip and self.hit and self.alive:
            dx = 2
        if self.flip == False and self.hit and self.alive:
            dx = -2

        self.rect.x += dx
        self.rect.y += dy
        self.health += self.regenrate

    def update(self):
        if self.health > 100:
            self.health = 100
        if self.health <= 0:
            self.regenrate = 0
            self.health = 0
            self.alive = False
            self.update_action(1)
        elif self.hit == True:
            if self.attacking == False:
                self.falsehit = True
            elif self.attacking == True:
                self.truehit = True
            self.hit = False
        elif self.falsehit == True:
            self.update_action(5)
        elif self.truehit == True:
            self.update_action(4)
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(0)
            elif self.attack_type == 2:
                self.update_action(0)
        elif self.running == True:
            self.update_action(3)
        else:
            self.update_action(2)

        animation_cooldown = 50

        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.animation_list[self.action]):
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                if self.action == 0:
                    self.attacking = False
                    self.attack_cooldown = 45   # 0.75 seconds at 60 FPS
                if self.action == 4:
                    self.truehit = False
                    self.attacking = False
                    self.attack_cooldown = 45   # 0.75 seconds at 60 FPS
                if self.action == 5:
                    self.falsehit = False
                    self.attacking = False
                    self.health += 20

        print(self.hit)


class Flyenemy(Monster):
    def __init__(self, name, x, y, flip, data, sprite_sheet, animation_steps, sound, statimg):
        super().__init__(name, x, y, flip, data, sprite_sheet, animation_steps, sound, statimg)
        self.flip = True
        self.alive = True
        self.damagetoken = 1
        self.rect = pygame.Rect((x, y, 80, 80))

    def move(self, screen_width, screen_height, surface, target, round_over, xpos):
        SPEED = 4   # Increased from 2
        GRAVITY = 0
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0
        self.xpos = xpos
        self.damage = 6   # Increased from 3

        if self.alive == True and self.attacking == False and round_over == False and self.rect.x - 200 >= self.xpos:
            dx = -SPEED
            self.running = True
            self.flip = True

        if self.rect.x - self.xpos < 300 and self.attack_cooldown == 0 and self.flip == True:
            self.attack(target)
            self.attack_type = 1

        if self.alive == True and round_over == False and self.attacking == False and self.rect.x + 200 <= self.xpos:
            dx = SPEED
            self.running = True
            self.flip = False

        if self.rect.x - self.xpos > -300 and self.attack_cooldown == 0 and self.flip == False:
            self.attack(target)
            self.attack_type = 1

        if self.attacking == True:
            if self.flip:
                dx = -30
            if self.flip == False:
                dx = 30

        # apply attack cooldown (frame-based, decrement by 1 per frame)
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # knockback
        if self.flip and self.hit and self.alive:
            dx = -20
        if self.flip == False and self.hit and self.alive:
            dx = 20

        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom

        self.rect.x += dx
        self.rect.y += dy

    def attack(self, target):
        if self.attack_cooldown == 0 and self.alive == True and target.health > 0 and self.attacking == False:
            self.attacking = True
            self.attack_sound.play()

        if self.attacking == True:
            hit = self.rect.colliderect(target.rect)
            if hit == True and self.damagetoken == 1:
                self.damagetoken = 0
                target.health -= self.damage
                print("Main MC HP " + str(target.health))
                target.hit = False
            elif self.damagetoken == 0:
                self.damagetoken = 1


class Wormenemy(Monster):
    def __init__(self, name, x, y, flip, data, sprite_sheet, animation_steps, sound, statimg, skill, screen):
        super().__init__(name, x, y, flip, data, sprite_sheet, animation_steps, sound, statimg)
        self.flip = True
        self.alive = True
        self.damagetoken = 1
        self.rect = pygame.Rect((x, y, 400, 500))
        self.skill = skill
        self.screen = screen
        self.action = 1
        self.health = 100
        # ── Worm is immune to player melee; only reflected fireballs hurt it ─
        self.melee_immune = True

    def move(self, screen_width, screen_height, surface, target, round_over, xpos):
        SPEED = 10
        GRAVITY = 0
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0
        self.xpos = xpos
        self.damage = 3

        if self.alive and target.alive:
            self.skill.draw(self.screen)
            self.skill.move(1366, 768, self.screen, target, False, xpos)
            self.skill.update(target, self)
        print(self.health)


class fireball(Monster):
    def __init__(self, name, x, y, flip, data, sprite_sheet, animation_steps, sound, statimg):
        super().__init__(name, x, y, flip, data, sprite_sheet, animation_steps, sound, statimg)
        self.flip = True
        self.alive = True
        self.rect = pygame.Rect((x, y, 90, 90))
        self.running = True
        self.exploding = False      # True while playing hit/explosion animation
        self.action = 1
        self.damage = 15
        self.damagetoken = 1
        self.speed = 13             # ── Faster travel speed (was 10) ──
        # ── Reflected fireball deals much more damage to the worm ──────────
        self.reflected_damage = 10  # was implicitly 5 in the old code
        self.launch_delay = 0       # Countdown before next launch (frames)
        self.LAUNCH_DELAY = 50      # ── Faster relaunch: 50 frames (~0.83s) was 90 (~1.5s) ──

    def _reset_position(self):
        """Reposition fireball at worm side, random height, with a short delay."""
        self.rect.x = 1050
        self.rect.y = random.randint(304, 600)
        self.flip = True
        self.running = False
        self.exploding = False
        self.damagetoken = 1
        self.launch_delay = self.LAUNCH_DELAY
        self.update_action(1)

    def move(self, screen_width, screen_height, surface, target, round_over, xpos):
        # Wait for launch delay to count down before moving
        if self.launch_delay > 0:
            self.launch_delay -= 1
            return
        if self.exploding:
            return  # Don't move while explosion animation plays

        self.running = True

        # Player reflects the fireball by attacking it
        if self.flip and self.rect.colliderect(target.attacking_rect) and target.attacking:
            self.flip = False   # Now travelling back toward worm
            self.damagetoken = 1

        # Move left (toward player) or right (reflected back)
        if self.flip:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

        # Left boundary — hit player side wall, reset
        if self.rect.right <= 0:
            self._reset_position()

        # Right boundary — reflected ball hits worm
        if self.rect.left >= screen_width:
            self._reset_position()

    def update(self, target, worm):
        if self.launch_delay > 0:
            return  # Waiting, nothing to animate yet

        # Check hit on player (only when travelling left toward player)
        if self.flip and self.running and not self.exploding:
            if self.rect.colliderect(target.rect) and self.damagetoken == 1:
                self.damagetoken = 0
                target.health -= self.damage
                target.hit = True
                self.exploding = True
                self.running = False
                self.update_action(0)   # Play explosion animation

        # Check reflected ball hitting worm (travelling right) — deals extra damage
        if not self.flip and self.running and not self.exploding:
            if self.rect.colliderect(worm.rect):
                worm.health -= self.reflected_damage   # ── was 5, now 25 ──
                worm.hit = True
                self._reset_position()
                return

        # After explosion animation finishes, relaunch
        if self.exploding and self.action == 0:
            if self.frame_index >= len(self.animation_list[0]) - 1:
                self._reset_position()

        animation_cooldown = 50
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = len(self.animation_list[self.action]) - 1

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))