import pygame
from newCharacters import Character, Monster_humanoid, Monster, Monster_Skeleton, Flyenemy, Wormenemy, fireball
from Items import Chest, Item, healplayer


pygame.init()

# gamewindow 16:9 res
screenWidth = 1366
screenHeight = 768
global screen
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Ancient Dungeon Quest")
clock = pygame.time.Clock()
FPS = 60

# Colors
ORANGE = (250, 174, 43)
MAIN_WHITE = (243, 210, 193)
RED = (250, 82, 70)
YELLOW = (255, 251, 159)
WHITE = (255, 255, 255)
BLACK = (15, 14, 23)
BLUE = (61, 169, 252)
BROWN = (110, 79, 51)

# Load Images
bg_image = pygame.image.load("assets/images/background/1ststage_bg.png").convert_alpha()
bg_image2 = pygame.image.load("assets/images/background/2ndstage_bg.png").convert_alpha()
bg_image3 = pygame.image.load("assets/images/background/3rdstage_bg.png").convert_alpha()
bg_image4 = pygame.image.load("assets/images/background/4thstage_bg.png").convert_alpha()
bg_image5 = pygame.image.load("assets/images/background/finalstage_bg.png").convert_alpha()
nextlvl = pygame.image.load("assets/images/UI/nlvl.png").convert_alpha()
logo_img = pygame.image.load("assets/images/icons/ADQ_LOGO.png").convert_alpha()
statsamurai = pygame.image.load("assets/images/UI/samuraistats.png").convert_alpha()
statwarrior = pygame.image.load("assets/images/UI/warriorstats.png").convert_alpha()
health_potion_img = pygame.image.load("assets/images/items/hp_potion.png").convert_alpha()
placeholder = pygame.image.load("assets/images/placeholder.png").convert_alpha()
samuraiimg = pygame.image.load("assets/images/UI/samurai_textbox.png").convert_alpha()
warriorimg = pygame.image.load("assets/images/UI/warrior_textbox.png").convert_alpha()
chat_box = pygame.image.load("assets/images/scroll.png").convert_alpha()
goblin_pic = pygame.image.load("assets/images/Monsters_Creatures_Fantasy/goblin_pic.png").convert_alpha()
eye_pic = pygame.image.load("assets/images/Monsters_Creatures_Fantasy/eye.png").convert_alpha()
skeleton_pic = pygame.image.load("assets/images/Monsters_Creatures_Fantasy/skeleton_pic.png").convert_alpha()
worm_pic = pygame.image.load("assets/images/Monsters_Creatures_Fantasy/worm.png").convert_alpha()
wizard_pic = pygame.image.load("assets/images/Monsters_Creatures_Fantasy/wizard.png").convert_alpha()

# Character Sheets
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
samurai_sheet = pygame.image.load("assets/images/samurai/Sprites/samurai.png").convert_alpha()
goblin_sheet = pygame.image.load("assets/images/Monsters_Creatures_Fantasy/Goblin/goblin.png").convert_alpha()
chest_sheet = pygame.image.load("assets/images/objects/chest.png").convert_alpha()
skeleton_sheet = pygame.image.load("assets/images/Monsters_Creatures_Fantasy/Skeleton/skeletonf.png").convert_alpha()
fly_sheet = pygame.image.load("assets/images/Monsters_Creatures_Fantasy/Flying eye/eye.png").convert_alpha()
worm_sheet = pygame.image.load("assets/images/Monsters_Creatures_Fantasy/Fire Worm/Sprites/Worm/worm.png").convert_alpha()
fireball_sheet = pygame.image.load("assets/images/fireball/ball1.png").convert_alpha()
fireball_sheetalt = pygame.image.load("assets/images/fireball/ballalt.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

# Sheet Animation Frames
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
SAMURAI_ANIMATION_STEPS = [8, 8, 2, 6, 6, 4, 6]
GOBLIN_ANIMATION_STEPS = [8, 4, 4, 8, 4]
SKELETON_ANIMATION_STEPS = [8, 4, 4, 4, 4, 4]
CHEST_ANIMATION_STEPS = [2]
FLY_ANIMATION_STEPS = [8, 4, 8, 8, 4]
WORM_ANIMATION_STEPS = [16, 8, 9, 9, 3]
FIREBALL_ANIMATION_STEPS = [7, 6]
WIZARD_ANIMATION_STEPS = [8, 8, 2, 8, 8, 3, 7]

# Character Frame Data
WARRIOR_SIZE = 162
WARRIOR_SCALE = 5
WARRIOR_OFFSET = [65, 60]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]

WIZARD_SIZE = 250
WIZARD_SCALE = 5
WIZARD_OFFSET = [120, 126]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

SAMURAI_SIZE = 200
SAMURAI_SCALE = 5
SAMURAI_OFFSET = [90, 80]
SAMURAI_DATA = [SAMURAI_SIZE, SAMURAI_SCALE, SAMURAI_OFFSET]

GOBLIN_SIZE = 150
GOBLIN_SCALE = 6
GOBLIN_OFFSET = [65, 70]
GOBLIN_DATA = [GOBLIN_SIZE, GOBLIN_SCALE, GOBLIN_OFFSET]

SKELETON_SIZE = 150
SKELETON_SCALE = 5
SKELETON_OFFSET = [65, 61]
SKELETON_DATA = [SKELETON_SIZE, SKELETON_SCALE, SKELETON_OFFSET]

FLY_SIZE = 150
FLY_SCALE = 5
FLY_OFFSET = [60, 70]
FLY_DATA = [FLY_SIZE, FLY_SCALE, FLY_OFFSET]

WORM_SIZE = 90
WORM_SCALE = 15
WORM_OFFSET = [30, 28]
WORM_DATA = [WORM_SIZE, WORM_SCALE, WORM_OFFSET]

CHEST_SIZE = 50
CHEST_SCALE = 5
CHEST_OFFSET = [90, 20]
CHEST_DATA = [CHEST_SIZE, CHEST_SCALE, CHEST_OFFSET]

BALL_SIZE = 46
BALL_SCALE = 5
BALL_OFFSET = [15, 10]
BALL_DATA = [BALL_SIZE, BALL_SCALE, BALL_OFFSET]

# Load Audio

# BGM
pygame.mixer.music.load("assets/audio/Jigoku.mp3")
pygame.mixer.music.set_volume(.1)
pygame.mixer.music.play(-1, 0.0, 500)
# BGM

sword_fx = pygame.mixer.Sound("assets/audio/samurai_sword.wav")
sword_fx.set_volume(0.1)
goblin_fx = pygame.mixer.Sound("assets/audio/goblin.mp3")
goblin_fx.set_volume(0.04)
bone_fx = pygame.mixer.Sound("assets/audio/bone.mp3")
bone_fx.set_volume(0.04)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
fly_fx = pygame.mixer.Sound("assets/audio/fly.mp3")
fly_fx.set_volume(0.04)
fire_fx = pygame.mixer.Sound("assets/audio/fireball.mp3")
fire_fx.set_volume(0.1)

# Fonts
sub_font = pygame.font.Font("assets/fonts/ancient.ttf", 110)
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
level_font = pygame.font.Font("assets/fonts/ancient.ttf", 37)
start_font = pygame.font.Font("assets/fonts/font_chase.ttf", 42)
char_font = pygame.font.Font("assets/fonts/font_chase.ttf", 20)
goblin_font = pygame.font.Font("assets/fonts/font_chase.ttf", 30)
mc_font = pygame.font.Font("assets/fonts/font_chase.ttf", 30)
game_over_font = pygame.font.Font("assets/fonts/ancient.ttf", 150)
pause_font = pygame.font.Font("assets/fonts/ancient.ttf", 30)
stat_font = pygame.font.Font("assets/fonts/ancient.ttf", 25)
stage_lvl_font = pygame.font.Font("assets/fonts/ancient.ttf", 40)
note_font = pygame.font.Font("assets/fonts/ancient.ttf", 25)
button_font = pygame.font.Font("assets/fonts/ancient.ttf", 45)


# Basic Functions & Classes

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


class Background():
    def __init__(self, img):
        self.img = img

    def draw(self):
        scaled_bg = pygame.transform.scale(self.img, (screenWidth, screenHeight))
        screen.blit(scaled_bg, (0, 0))


def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, YELLOW, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


def draw_mana_bar(mana, x, y):
    ratio = mana / 100
    pygame.draw.rect(screen, MAIN_WHITE, (x - 2, y - 2, 404, 19))
    pygame.draw.rect(screen, RED, (x, y, 400, 15))
    pygame.draw.rect(screen, BLUE, (x, y, 400 * ratio, 15))


def draw_health_gob(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, MAIN_WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


def draw_health_boss(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, MAIN_WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


class Image():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), (int(height * scale))))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.active = False

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update_nlvl(self, player):
        if player.interact == True and self.rect.colliderect(player.rect):
            self.active = True
        else:
            self.active = False


# ── End-screen button (drawn entirely with pygame, no image asset needed) ────
class EndButton():
    """A simple rounded-rect button for the victory end screen."""

    def __init__(self, x, y, width, height, label, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.color = color
        self.hover_color = hover_color
        self.clicked = False  # edge-triggered; reset each frame by caller

    def draw(self):
        pos = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(pos)
        current_color = self.hover_color if hovered else self.color

        # Draw drop-shadow
        shadow_rect = self.rect.move(4, 4)
        pygame.draw.rect(screen, BLACK, shadow_rect, border_radius=12)

        # Draw main body
        pygame.draw.rect(screen, current_color, self.rect, border_radius=12)

        # Border
        pygame.draw.rect(screen, WHITE, self.rect, 3, border_radius=12)

        # Centred label
        text_surf = button_font.render(self.label, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        """Return True once per left-button-up inside the rect."""
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


# Button x positions: centred pair around the middle of the screen
_BTN_W, _BTN_H = 200, 55   # reduced size
_BTN_Y = screenHeight // 2 + 240
_BTN_GAP = 30                            
_total_w = _BTN_W * 2 + _BTN_GAP
_btn_left_x = screenWidth // 2 - _total_w // 2

retry_button = EndButton(
    _btn_left_x, _BTN_Y,
    _BTN_W, _BTN_H,
    "Retry",
    (60, 120, 60),       # dark green
    (90, 180, 90),       # light green on hover
)

exit_button = EndButton(
    _btn_left_x + _BTN_W + _BTN_GAP, _BTN_Y,
    _BTN_W, _BTN_H,
    "Exit",
    (140, 30, 30),       # dark red
    (210, 60, 60),       # light red on hover
)
# ─────────────────────────────────────────────────────────────────────────────


# Create Objects from Image Class
nlvl = Image(1100, 450, nextlvl, 1)
logo = Image(540, -60, logo_img, .13)
sam = Image(540, -60, samuraiimg, .13)
war = Image(540, -60, warriorimg, .13)
dialogue_box = Image(280, 380, chat_box, .36)
goblin_frame = Image(1255, 20, goblin_pic, .09)
eye_frame = Image(1230, 17, eye_pic, .12)
skeleton_frame = Image(1240, 20, skeleton_pic, .1)
worm_frame = Image(1250, 20, worm_pic, .1)
wizard_frame = Image(1270, 30, wizard_pic, .15)


# General Objects
# Players
samurai_1 = Character("p1", 210, 480, False, SAMURAI_DATA, samurai_sheet, SAMURAI_ANIMATION_STEPS, sword_fx, statsamurai)
warrior_1 = Character("p2", 210, 480, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx, statwarrior)


# Enemies
def goblintype():
    goblin = Monster(4, 1000, 480, True, GOBLIN_DATA, goblin_sheet, GOBLIN_ANIMATION_STEPS, goblin_fx, placeholder)
    return goblin


def skeletontype():
    skeleton = Monster_Skeleton(8, 1000, 480, True, SKELETON_DATA, skeleton_sheet, SKELETON_ANIMATION_STEPS, bone_fx, placeholder)
    return skeleton


def flytype():
    fly = Flyenemy(8, 1000, 520, True, FLY_DATA, fly_sheet, FLY_ANIMATION_STEPS, fly_fx, placeholder)
    return fly


def wormtype():
    worm = Wormenemy(8, 1000, 245, True, WORM_DATA, worm_sheet, WORM_ANIMATION_STEPS, fly_fx, placeholder, createfireball(), screen)
    return worm


def createfireball():
    fireballproj = fireball(8, 1000, 245, True, BALL_DATA, fireball_sheet, FIREBALL_ANIMATION_STEPS, fire_fx, placeholder)
    return fireballproj


def wizardtype():
    wizard = Monster_humanoid("wiz", 1000, 520, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, fire_fx, placeholder)
    return wizard


# Items
def createpotion():
    hp_potion = Item(540, 550, health_potion_img, .055, healplayer)
    return hp_potion


# Chests
chest1 = Chest(7, 1000, 613, False, CHEST_DATA, chest_sheet, CHEST_ANIMATION_STEPS, sword_fx, createpotion())
chest2 = Chest(7, 1000, 613, False, CHEST_DATA, chest_sheet, CHEST_ANIMATION_STEPS, sword_fx, createpotion())
chest3 = Chest(7, 1000, 613, False, CHEST_DATA, chest_sheet, CHEST_ANIMATION_STEPS, sword_fx, createpotion())
chest4 = Chest(7, 1000, 613, False, CHEST_DATA, chest_sheet, CHEST_ANIMATION_STEPS, sword_fx, createpotion())
chest5 = Chest(7, 1000, 613, False, CHEST_DATA, chest_sheet, CHEST_ANIMATION_STEPS, sword_fx, createpotion())


# Function for Changing stages
def lvlcheck():
    if stage == 1:
        stagebg = bg1
        return stagebg
    elif stage == 2:
        stagebg = bg2
        return stagebg
    elif stage == 3:
        stagebg = bg3
        return stagebg
    elif stage == 4:
        stagebg = bg5
        return stagebg
    elif stage == 5:
        stagebg = bg4
        return stagebg


def topUI(player, enemy):
    if stage == 1:
        draw_health_bar(player.health, 90, 30)
        draw_text("Haruki  ", mc_font, MAIN_WHITE, 90, 100)
        draw_text("  Class: Ronin  " + " Level: 1", char_font, WHITE, 212, 105)
        draw_mana_bar(player.mana, 90, 65)
        draw_text("", level_font, BLUE, 105, 70)

        draw_text("STAGE 1", stage_lvl_font, RED, 620, 90)

        draw_health_gob(enemy.health, 860, 45)
        draw_text("Goblin the thief ", goblin_font, MAIN_WHITE, 855, 90)
        draw_text(" Class: Monster " + " Level : 2", char_font, WHITE, 950, 130)
        goblin_frame.draw()

    elif stage == 2:
        draw_health_bar(player.health, 90, 30)
        draw_text("Haruki  ", mc_font, MAIN_WHITE, 90, 110)
        draw_text("  Class: Ronin  " + " Level: 3", char_font, WHITE, 212, 115)
        draw_mana_bar(player.mana, 90, 65)
        draw_text("", level_font, BLUE, 105, 70)

        draw_text("STAGE 2", stage_lvl_font, RED, 620, 90)

        draw_health_gob(enemy.health, 860, 45)
        draw_text("One-Eyed Banshee Bat", goblin_font, MAIN_WHITE, 855, 90)
        draw_text(" Class: Monster " + " Level : 4", char_font, WHITE, 950, 140)
        eye_frame.draw()

    elif stage == 3:
        draw_health_bar(player.health, 90, 30)
        draw_text("Haruki  ", mc_font, MAIN_WHITE, 90, 110)
        draw_text("  Class: Ronin  " + " Level: 6", char_font, WHITE, 212, 115)
        draw_mana_bar(player.mana, 90, 65)
        draw_text("", level_font, BLUE, 105, 70)

        draw_text("STAGE 3", stage_lvl_font, RED, 620, 90)

        draw_health_gob(enemy.health, 860, 45)
        draw_text("Undead Warrior", goblin_font, MAIN_WHITE, 855, 90)
        draw_text(" Class: Monster " + " Level : 7", char_font, WHITE, 950, 140)
        skeleton_frame.draw()

    elif stage == 4:
        draw_health_bar(player.health, 90, 30)
        draw_text("Haruki  ", mc_font, MAIN_WHITE, 90, 110)
        draw_text("  Class: Ronin  " + " Level: 8", char_font, WHITE, 212, 115)
        draw_mana_bar(player.mana, 90, 65)
        draw_text("", level_font, BLUE, 105, 70)

        draw_text("STAGE 4", stage_lvl_font, RED, 620, 90)
        draw_health_boss(enemy.health, 860, 45)
        draw_text("Scorching abyss Worm", goblin_font, MAIN_WHITE, 855, 90)
        draw_text(" Class: Monster " + " Level : 10", char_font, WHITE, 950, 140)
        worm_frame.draw()

    elif stage == 5:
        draw_health_bar(player.health, 90, 30)
        draw_text("Haruki  ", mc_font, MAIN_WHITE, 90, 110)
        draw_text("  Class: Ronin  " + " Level: 10", char_font, WHITE, 212, 115)
        draw_mana_bar(player.mana, 90, 65)
        draw_text("", level_font, BLUE, 105, 70)

        draw_text("FINAL BOSS", stage_lvl_font, RED, 600, 90)

        draw_health_boss(enemy.health, 860, 45)
        draw_text("Corrupted Sorcerer", goblin_font, MAIN_WHITE, 855, 90)
        draw_text(" Class: Monster " + " Level : 15", char_font, WHITE, 950, 140)
        wizard_frame.draw()


class Stage():
    def __init__(self, player, enemy, chest, levelindex):
        self.player = player
        self.enemy = enemy
        self.chest = chest
        self.levelindex = levelindex
        self.initx = player.xloc
        player.rect.x = self.initx
        self.starttoken = 1
        self.initx2 = enemy.rect.x
        self.enemyinithealth = enemy.health
        self.playerinithealth = player.health
        # Retry countdown: -1 means not counting down
        self.retry_countdown = -1
        self.retry_start_time = 0

    def restart(self):
        # Begin a 3-second countdown before actually restarting
        self.retry_countdown = 3
        self.retry_start_time = pygame.time.get_ticks()

    def _do_restart(self):
        # Actually reset everything once countdown finishes
        self.player.alive = True
        self.player.health = self.playerinithealth
        self.player.mana = 100
        self.player.rect.x = self.initx
        self.player.x = 100
        self.player.attacking = False
        self.player.attack_cooldown = 45   # 1s lock on spawn
        self.enemy.rect.x = self.initx2
        self.enemy.health = self.enemyinithealth
        self.enemy.alive = True
        self.enemy.attacking = False
        self.enemy.attack_cooldown = 45   # 1s lock on spawn
        self.starttoken = 1
        self.retry_countdown = -1

    # Start Level
    def levelstart(self):
        global level

        # Handle retry countdown
        if self.retry_countdown > 0:
            elapsed = pygame.time.get_ticks() - self.retry_start_time
            self.retry_countdown = 3 - int(elapsed / 1000)
            draw_text(str(max(self.retry_countdown, 1)), count_font, RED, screenWidth / 2, screenHeight / 3)
            if elapsed >= 3000:
                self._do_restart()
            return self.levelindex

        if self.starttoken == 1:
            self.player.rect.x = self.initx
            # Lock attacks for 1.5s (90 frames) at level start
            self.player.attack_cooldown = 45
            self.enemy.attack_cooldown = 45
            self.starttoken = 0

        topUI(self.player, self.enemy)
        self.player.move(screenWidth, screenHeight, screen, self.enemy, round_over)
        self.enemy.move(screenWidth, screenHeight, screen, self.player, round_over, self.player.rect.x)

        self.player.update()
        self.player.draw(screen)

        self.enemy.update()
        self.enemy.draw(screen)

        if round_over == False:
            if self.player.alive == False:
                draw_text("Game Over.. Press R to retry level.", pause_font, WHITE, screenWidth // 2 - 210, screenHeight // 1.1)
                key = pygame.key.get_pressed()
                if key[pygame.K_r] and self.retry_countdown == -1:
                    self.restart()

            if self.enemy.alive == False:
                nlvl.draw()
                nlvl.update_nlvl(self.player)
                draw_text("Enemy Defeated", game_over_font, MAIN_WHITE, 250, 290)
                self.chest.draw(screen)
                self.chest.update(self.player)
                if self.chest.open == True:
                    self.chest.item.draw()
                    self.chest.item.update(self.player)
                    self.chest.item.gravity()
                if nlvl.active == True:
                    self.levelindex += 1
                    return self.levelindex
            else:
                self.levelindex = self.levelindex

        return self.levelindex

    # Start Final Level
    def levelstartfin(self):
        global level, game_run, stage, Select, check, intro_count, last_count_update
        global level1, level2, level3, level4, level5
        global chest1, chest2, chest3, chest4, chest5

        # Handle retry countdown
        if self.retry_countdown > 0:
            elapsed = pygame.time.get_ticks() - self.retry_start_time
            self.retry_countdown = 3 - int(elapsed / 1000)
            draw_text(str(max(self.retry_countdown, 1)), count_font, RED, screenWidth / 2, screenHeight / 3)
            if elapsed >= 3000:
                self._do_restart()
            return self.levelindex

        if self.starttoken == 1:
            self.player.rect.x = self.initx
            # Lock attacks for 1.5s (90 frames) at level start
            self.player.attack_cooldown = 45
            self.enemy.attack_cooldown = 45
            self.starttoken = 0

        topUI(self.player, self.enemy)
        self.player.move(screenWidth, screenHeight, screen, self.enemy, round_over)
        self.enemy.move(screenWidth, screenHeight, screen, self.player, round_over, self.player.rect.x)

        self.player.update()
        self.player.draw(screen)

        self.enemy.update()
        self.enemy.draw(screen)

        if round_over == False:
            if self.player.alive == False:
                draw_text("Game Over.. Press R to retry level.", pause_font, WHITE, screenWidth // 2 - 230, screenHeight // 1.1)
                key = pygame.key.get_pressed()
                if key[pygame.K_r] and self.retry_countdown == -1:
                    self.restart()

            if self.enemy.alive == False:
                # ── Victory screen ────────────────────────────────────────
                draw_text("VICTORY!", game_over_font, MAIN_WHITE, 400, 250)
                dialogue_box.draw()
                draw_text("Congratulations, you did well escaping from the dungeon",
                          note_font, RED, screenWidth // 2 - 200, screenHeight // 1.51)
                draw_text("or did you actually escape from it ?",
                          note_font, RED, screenWidth // 2 - 150, screenHeight // 1.41)
                draw_text("Let's find more on Ancient Dungeon Quest 2",
                          note_font, RED, screenWidth // 2 - 180, screenHeight // 1.31)

                retry_button.draw()
                exit_button.draw()

                # NOTE: button click events are handled in the main event loop
                # via the global `pending_retry` / `pending_exit` flags below.
            else:
                self.levelindex = self.levelindex

        return self.levelindex


# Create Stage/BG
bg1 = Background(bg_image)
bg2 = Background(bg_image2)
bg3 = Background(bg_image3)
bg4 = Background(bg_image4)
bg5 = Background(bg_image5)


class Button():
    def __init__(self, x, y, image, scale, name):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), (int(height * scale))))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.active = False
        self.x = x
        self.y = y
        self.name = name
        self.clicked = False

    def draw_text(self, text, color, x, y):
        font = pygame.font.Font("assets/fonts/ancient.ttf", 25)
        img = font.render(text, True, color)
        screen.blit(img, (x, y))

    def draw(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.draw_text(self.name, WHITE, self.x + 70, self.y + 203)

            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.active = True
                toggle_select()

        screen.blit(self.image, (self.rect.x, self.rect.y))


# Create Buttons
selectSam = Button((screenWidth / 3) + 30, 200, samuraiimg, .5, "Samurai")
selectWar = Button((screenWidth / 2) + 30, 200, warriorimg, .5, "Warrior")


def pauseScreen(player):
    draw_text("Game Paused.. Press ESCAPE to Unpause.", pause_font, WHITE, screenWidth // 2 - 230, screenHeight // 1.1)
    screen.blit(player.statimg, (100, 100))
    draw_text("Attack:{}".format(player.damage), stat_font, BROWN, 142, 365)
    draw_text("Defense", stat_font, BROWN, 142, 395)
    draw_text("Stamina:{}".format(player.mana), stat_font, BROWN, 142, 425)
    draw_text("Health:{}".format(player.health), stat_font, BROWN, 142, 455)
    draw_text("Name:{}".format(player.name), stat_font, BROWN, 240, 365)


def charaSelect():
    draw_text("Select Your Character", pause_font, WHITE, screenWidth // 2 - 100, screenHeight // 5)
    selectSam.draw()
    selectWar.draw()

    if selectSam.active == True:
        player = samurai_1
        return player

    if selectWar.active == True:
        player = warrior_1
        return player


def full_game_reset():
    """Reset everything back to Stage 1 (called by the Retry button on victory screen)."""
    global stage, intro_count, last_count_update
    global chest1, chest2, chest3, chest4, chest5
    global level1, level2, level3, level4, level5

    stage = 1
    intro_count = 3
    last_count_update = pygame.time.get_ticks()

    # Recreate chests (they track open/used state)
    chest1 = Chest(7, 1000, 613, False, CHEST_DATA, chest_sheet, CHEST_ANIMATION_STEPS, sword_fx, createpotion())
    chest2 = Chest(7, 1000, 613, False, CHEST_DATA, chest_sheet, CHEST_ANIMATION_STEPS, sword_fx, createpotion())
    chest3 = Chest(7, 1000, 613, False, CHEST_DATA, chest_sheet, CHEST_ANIMATION_STEPS, sword_fx, createpotion())
    chest4 = Chest(7, 1000, 613, False, CHEST_DATA, chest_sheet, CHEST_ANIMATION_STEPS, sword_fx, createpotion())
    chest5 = Chest(7, 1000, 613, False, CHEST_DATA, chest_sheet, CHEST_ANIMATION_STEPS, sword_fx, createpotion())

    # Recreate all stage objects (enemies need fresh state too)
    level1 = Stage(player, goblintype(), chest1, 1)
    level2 = Stage(player, flytype(), chest2, 2)
    level3 = Stage(player, skeletontype(), chest3, 3)
    level4 = Stage(player, wormtype(), chest4, 4)
    level5 = Stage(player, wizardtype(), chest5, 5)

    # Reset player fully
    player.alive = True
    player.health = 100
    player.mana = 100
    player.rect.x = player.xloc
    player.attacking = False
    player.attack_cooldown = 0


# Game Variables
start_menu = True
game_run = True
paused = False
stage = 1
stagebg = bg1
intro_count = 3
last_count_update = pygame.time.get_ticks()
level = 1
round_over = False
ROUND_OVER_COOLDOWN = 2000
Select = True
check = False
player = None

# Flags set inside the event loop and consumed by game logic
pending_retry = False
pending_exit = False

# Stage objects (populated after character select)
level1 = level2 = level3 = level4 = level5 = None


def toggle_select():
    global Select, check
    Select = not Select
    check = not check


# Game Loop
while game_run:

    clock.tick(FPS)

    stagebg = lvlcheck()
    Background.draw(stagebg)
    logo.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if player is not None:
                    paused = not paused

        # ── Victory screen button clicks ──────────────────────────────────
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # Only active when we're on the final victory screen
            if (stage == 5 and level5 is not None
                    and not level5.enemy.alive):
                if retry_button.is_clicked(event):
                    pending_retry = True
                if exit_button.is_clicked(event):
                    pending_exit = True

    # Process deferred actions (must happen outside the event loop)
    if pending_exit:
        game_run = False
        pending_exit = False

    if pending_retry and player is not None:
        full_game_reset()
        pending_retry = False

    if paused and player is not None:
        pauseScreen(player)

    if not paused:

        if start_menu:
            Background.draw(stagebg)
            draw_text("Ancient Dungeon Quest", sub_font, ORANGE, screenWidth // 2 - 420, screenHeight // 2.8)
            draw_text("Press", start_font, MAIN_WHITE, screenWidth // 2 - 310, screenHeight // 1.25)
            draw_text("SPACE", start_font, RED, screenWidth // 2 - 140, screenHeight // 1.25)
            draw_text("to Start", start_font, MAIN_WHITE, screenWidth // 1 - 655, screenHeight // 1.25)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                start_menu = False

        elif Select == True:
            player = charaSelect()
            dialogue_box.draw()
            draw_text("Embark on a thrilling journey in Ancient Dungeon Quest, a riveting escape ", note_font, BLACK, screenWidth // 2 - 300, screenHeight // 1.60)
            draw_text("game where players find themselves trapped within the depths of an ", note_font, BLACK, screenWidth // 2 - 300, screenHeight // 1.50)
            draw_text("enigmatic and ancient dungeon. Immerse yourself, each level challenges", note_font, BLACK, screenWidth // 2 - 300, screenHeight // 1.40)
            draw_text("players with progressively complex and unique enemies", note_font, BLACK, screenWidth // 2 - 300, screenHeight // 1.31)
            draw_text("Escape or fight the choice is yours", note_font, RED, screenWidth // 2 - 150, screenHeight // 1.21)
            if check == True:
                level1 = Stage(player, goblintype(), chest1, 1)
                level2 = Stage(player, flytype(), chest2, 2)
                level3 = Stage(player, skeletontype(), chest3, 3)
                level4 = Stage(player, wormtype(), chest4, 4)
                level5 = Stage(player, wizardtype(), chest5, 5)

        elif start_menu == False and Select == False:
            if intro_count <= 0 and stage == 1:
                stage = level1.levelstart()
            elif intro_count <= 0 and stage == 2:
                stage = level2.levelstart()
            elif intro_count <= 0 and stage == 3:
                stage = level3.levelstart()
            elif intro_count <= 0 and stage == 4:
                stage = level4.levelstart()
            elif intro_count <= 0 and stage == 5:
                stage = level5.levelstartfin()
            else:
                draw_text(str(intro_count), count_font, RED, screenWidth / 2, screenHeight / 3)
                if (pygame.time.get_ticks() - last_count_update) >= 1000:
                    intro_count -= 1
                    last_count_update = pygame.time.get_ticks()

    pygame.display.update()

pygame.quit()