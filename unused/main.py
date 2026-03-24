import pygame
from Textbasedtest import Character, Monster_humanoid,Monster,Monster_Skeleton
from Items import Chest, Item,healplayer

pygame.init()

# create game window
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ancient Dungeon Quest")

# set framerate
clock = pygame.time.Clock()
FPS = 60

# define colours
ORANGE = (250,174,43)
MAIN_WHITE = (243,210,193)
RED = (250, 82, 70)
YELLOW = (255,251,159)
WHITE = (255, 255, 255)
BLACK = (15,14,23)
BLUE = (61,169,252)
GOBLIN_COLOR = (144,238,144)

# define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
level = 1  # player scores. [P1]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# define fighter variables-----------------------------------------------------------------------------------Sprite
WARRIOR_SIZE = 162
WARRIOR_SCALE = 5
WARRIOR_OFFSET = [90, 55]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]


SAMURAI_SIZE= 200
SAMURAI_SCALE= 5
SAMURAI_OFFSET=[90, 80]
SAMURAI_DATA=[SAMURAI_SIZE, SAMURAI_SCALE, SAMURAI_OFFSET]

GOBLIN_SIZE= 150
GOBLIN_SCALE= 6
GOBLIN_OFFSET=[65,70]
GOBLIN_DATA=[GOBLIN_SIZE,GOBLIN_SCALE,GOBLIN_OFFSET]

SKELETON_SIZE=150
SKELETON_SCALE=5
SKELETON_OFFSET=[65,61]
SKELETON_DATA=[SKELETON_SIZE,SKELETON_SCALE,SKELETON_OFFSET]
'''
MUSH_SIZE=
MUSH_SCALE=
MUSH_OFFSET=
MUSH_DATA=

EYE_SIZE=
EYE_SCALE=
EYE_OFFSET=
EYE_DATA=
'''
CHEST_SIZE=50
CHEST_SCALE=5
CHEST_OFFSET=[90,20]
CHEST_DATA=[CHEST_SIZE,CHEST_SCALE,CHEST_OFFSET]


# load music and sounds
pygame.mixer.music.load("assets/audio/Jigoku.mp3") 
pygame.mixer.music.set_volume(.1)
pygame.mixer.music.play(-1, 0.0, 500)

sword_fx = pygame.mixer.Sound("assets/audio/samurai_sword.wav")
sword_fx.set_volume(0.1)

goblin_fx = pygame.mixer.Sound("assets/audio/goblin.mp3")
goblin_fx.set_volume(0.04)

bone_fx = pygame.mixer.Sound("assets/audio/bone.mp3")
bone_fx.set_volume(0.04)

magic_fx= pygame.mixer.Sound("assets/audio/magic.wav")

# load background image
bg_image = pygame.image.load("assets/images/background/1ststage_bg.png").convert_alpha()
bg_image2 = pygame.image.load("assets/images/background/2ndstage_bg.png").convert_alpha()
bg_image3 = pygame.image.load("assets/images/background/3rdstage_bg.png").convert_alpha()
bg_image4 = pygame.image.load("assets/images/background/4thstage_bg.png").convert_alpha()
bg_image5 = pygame.image.load("assets/images/background/finalstage_bg.png").convert_alpha()
nextlvl= pygame.image.load("assets/images/UI/nlvl.png").convert_alpha()
logo_img = pygame.image.load("assets/images/icons/ADQ_LOGO.png").convert_alpha()
health_potion_img = pygame.image.load("assets/images/items/hp_potion.png").convert_alpha()

# load spritesheets-----------------------------------------------------------------------------------------------------Images Dito
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
samurai_sheet= pygame.image.load("assets/images/samurai/Sprites/samurai.png").convert_alpha()
goblin_sheet= pygame.image.load("assets/images/Monsters_Creatures_Fantasy/Goblin/goblin.png").convert_alpha()
chest_sheet = pygame.image.load("assets/images/objects/chest.png").convert_alpha()
skeleton_sheet= pygame.image.load("assets/images/Monsters_Creatures_Fantasy/Skeleton/skeletonf.png").convert_alpha()



# define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
SAMURAI_ANIMATION_STEPS = [8, 8, 2, 6, 6, 4, 6]
GOBLIN_ANIMATION_STEPS = [8,4,4,8,4]
SKELETON_ANIMATION_STEPS = [8,4,4,4,4,4]
CHEST_ANIMATION_STEPS=[2]

# define font----------------------------------------------------------------------------------Font Dito
sub_font =   pygame.font.Font("assets/fonts/ancient.ttf", 110)
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
level_font = pygame.font.Font("assets/fonts/ancient.ttf", 37)
start_font = pygame.font.Font("assets/fonts/font_chase.ttf", 42)
char_font = pygame.font.Font("assets/fonts/font_chase.ttf", 19)
goblin_font = pygame.font.Font("assets/fonts/font_chase.ttf", 30)
mc_font = pygame.font.Font("assets/fonts/font_chase.ttf", 30)
game_over_font = pygame.font.Font("assets/fonts/ancient.ttf", 150)
pause_font= pygame.font.Font("assets/fonts/ancient.ttf", 30)

   

# function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
#bgclass
class Background():
    def __init__(self,img):
        self.img=img
    
           
# function for drawing background
    def draw(self):
        scaled_bg = pygame.transform.scale(self.img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_bg, (0, 0))
    

# function for drawing fighter health bar
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, YELLOW, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

# function for drawing fighter mana bar
def draw_mana_bar(mana, x, y):
    ratio = mana / 100
    pygame.draw.rect(screen, MAIN_WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, BLUE, (x, y, 400 * ratio, 30))
    
# function for drawing goblin health bar
def draw_health_gob(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, MAIN_WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

 #dito na HP at mana bar
def topUI(player,enemy):

    draw_health_bar(player.health, 90, 30)
    draw_text("Haruki  ", mc_font, MAIN_WHITE, 90, 110)
    draw_text("  Class: Ronin  " + " Level: " + str(level), char_font, WHITE, 212, 115)

            
    draw_mana_bar(player.mana, 90, 65)
    draw_text("",level_font, BLUE, 105, 70)
        
    draw_health_gob(enemy.health, 860, 45)
    draw_text("Goblin ",goblin_font, MAIN_WHITE, 855, 110)
    draw_text(" Class: Monster " + " Level : 1", char_font, WHITE, 982, 115)
    


# put img on screen func
class Image():
    def __init__(self,x,y,image,scale):
        width= image.get_width()
        height=image.get_height()
        self.image = pygame.transform.scale(image,(int(width*scale),(int(height*scale))))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.active=False
        
    def draw(self):
        screen.blit(self.image,(self.rect.x,self.rect.y))
        
    def update_nlvl(self, player):
        # check what action the player is performing
        if player.interact == True and player.rect.x >=1000:
            self.active=True
        else:
            self.active=False
    
         
nlvl= Image(1100,450,nextlvl,1)
logo = Image(540, -40, logo_img, .13) 
def createpotion():
    hp_potion = Item(540, 550, health_potion_img, .055,healplayer)
    return hp_potion
      
# create two instances of fighters------------------------------------------------------------------------------------Character/monster/chest creator
samurai_1 = Character(3, 210, 480, False, SAMURAI_DATA, samurai_sheet, SAMURAI_ANIMATION_STEPS, sword_fx)
goblin = Monster(4,1000,480,True,GOBLIN_DATA,goblin_sheet,GOBLIN_ANIMATION_STEPS, goblin_fx)
goblin2= Monster(6,1000,480,True,GOBLIN_DATA,goblin_sheet,GOBLIN_ANIMATION_STEPS, goblin_fx)
goblin3= Monster(6,1000,480,True,GOBLIN_DATA,goblin_sheet,GOBLIN_ANIMATION_STEPS, goblin_fx)
goblin4= Monster(6,1000,480,True,GOBLIN_DATA,goblin_sheet,GOBLIN_ANIMATION_STEPS, goblin_fx)
goblin5= Monster(6,1000,480,True,GOBLIN_DATA,goblin_sheet,GOBLIN_ANIMATION_STEPS, goblin_fx)
skeleton=Monster_Skeleton(8,1000,480,True,SKELETON_DATA,skeleton_sheet,SKELETON_ANIMATION_STEPS,bone_fx)
chest1=  Chest(5,1000,613,False,CHEST_DATA,chest_sheet,CHEST_ANIMATION_STEPS,sword_fx,createpotion())
chest2=  Chest(7,1000,613,False,CHEST_DATA,chest_sheet,CHEST_ANIMATION_STEPS,sword_fx,createpotion())
chest3=  Chest(7,1000,613,False,CHEST_DATA,chest_sheet,CHEST_ANIMATION_STEPS,sword_fx,createpotion())
chest4=  Chest(7,1000,613,False,CHEST_DATA,chest_sheet,CHEST_ANIMATION_STEPS,sword_fx,createpotion())
chest5=  Chest(7,1000,613,False,CHEST_DATA,chest_sheet,CHEST_ANIMATION_STEPS,sword_fx,createpotion())


#class for making stages

#Class stage---------------------------------------------------------------------------------Dito Stage class
class Stage():
    def __init__(self,player,enemy,chest,levelindex):
        self.player = player
        self.enemy= enemy
        self.chest=chest
        self.levelindex= levelindex
        self.initx= player.xloc
        player.rect.x= self.initx
        self.starttoken=1
    def levelstart(self):
        global level
        if self.starttoken==1:
            self.player.rect.x= self.initx
            self.starttoken=0

        topUI(self.player,self.enemy)
        self.player.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, self.enemy, round_over)
        self.enemy.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen,  self.player, round_over,self.player.rect.x)


        self.player.update()
        self.player.draw(screen)

        self.enemy.update()
        self.enemy.draw(screen)

        #for debugging----------------------------------------------------------------for debugging

        if self.enemy.attacking:
            self.enemy.draw_attacking_rect(screen)

        self.enemy.draw_goblin_rect(screen)

        if self.player.attacking:
            self.player.draw_attacking_rect(screen)

        self.player.draw_character_rect(screen)
    



        #for debugging----------------------------------------------------------------for debugging
        if round_over == False:
            if self.player.alive == False:
                draw_text("GAME OVER", game_over_font, RED, 450, 290)

            if self.enemy.alive == False :
                nlvl.draw()
                nlvl.update_nlvl(self.player)
                draw_text("LEVEL UP!", game_over_font, MAIN_WHITE, 400, 290)
                self.chest.draw(screen)
                self.chest.update(samurai_1)
                if self.chest.open==True:
                    self.chest.item.draw()
                    self.chest.item.update(self.player)
                    self.chest.item.gravity()
                if nlvl.active==True:
                    self.levelindex+=1
                    return self.levelindex
            else:
                self.levelindex=self.levelindex

                

        return self.levelindex
    def levelstartfin(self):
        global level
        if self.starttoken==1:
            self.player.rect.x= self.initx
            self.starttoken=0

        topUI(self.player,self.enemy)
        self.player.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, self.enemy, round_over)
        self.enemy.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen,  self.player, round_over,self.player.rect.x)


        self.player.update()
        self.player.draw(screen)

        self.enemy.update()
        self.enemy.draw(screen)


        if round_over == False:
            if self.player.alive == False:
                draw_text("GAME OVER", game_over_font, RED, 450, 290)

            if self.enemy.alive == False:
                draw_text("VICTORY!", game_over_font, MAIN_WHITE, 400, 290)
            else:
                self.levelindex=self.levelindex

                

        return self.levelindex

#Stage/Background Creator------------------Stage/Background Creator
level1= Stage(samurai_1,goblin,chest1,1)
level2= Stage(samurai_1,skeleton,chest2,2)
level3= Stage(samurai_1,goblin3,chest3,3)
level4= Stage(samurai_1,goblin4,chest4,4)
level5= Stage(samurai_1,goblin5,chest5,5)
bg1=Background(bg_image)
bg2=Background(bg_image2)
bg3=Background(bg_image3)
bg4=Background(bg_image4)
bg5=Background(bg_image5)

start_menu = True
game_run = True
paused = False
stage=1
stagebg=bg1

def lvlcheck():
    if stage ==1:
        stagebg=bg1
        return stagebg
    elif stage==2:
        stagebg=bg2
        return stagebg
    elif stage==3:
        stagebg=bg3
        return stagebg
    elif stage==4:
        stagebg=bg4
        return stagebg
    elif stage==5:
        stagebg=bg5
        return stagebg
#gameloop            
while game_run:

    clock.tick(FPS)
    
    stagebg=lvlcheck()
    
    Background.draw(stagebg)
    logo.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
    if paused:
        draw_text("Game Paused.. Press ESCAPE to Unpause.", pause_font, WHITE, SCREEN_WIDTH // 2 - 230, SCREEN_HEIGHT // 2)

    if not paused:

        if start_menu:
            
            Background.draw(stagebg)
            
            draw_text("Ancient Dungeon Quest", sub_font, ORANGE, SCREEN_WIDTH // 2 - 420, SCREEN_HEIGHT // 2.8)
            draw_text("Press", start_font, MAIN_WHITE, SCREEN_WIDTH // 2 - 310, SCREEN_HEIGHT // 1.25)
            draw_text("SPACE", start_font, RED, SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 1.25)
            draw_text("to Start", start_font, MAIN_WHITE, SCREEN_WIDTH // 1 - 655, SCREEN_HEIGHT // 1.25)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                start_menu = False

        elif start_menu== False:
            if intro_count <= 0 and stage==1:
                stage=level1.levelstart()
            elif intro_count <= 0 and stage==2:
                stage=level2.levelstart()
            elif intro_count <= 0 and stage==3:
                stage=level3.levelstart()
            elif intro_count <= 0 and stage==4:
                stage=level4.levelstart()
            elif intro_count <= 0 and stage==5:
                stage=level5.levelstartfin()
            else:
                draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
                if (pygame.time.get_ticks() - last_count_update) >= 1000:
                    intro_count -= 1
                    last_count_update = pygame.time.get_ticks()


    pygame.display.update()

pygame.quit()

