import pygame

class Character():
  def __init__(self, name, x, y, flip, data, sprite_sheet, animation_steps, sound):
    self.name = name
    self.size = data[0]
    self.image_scale = data[1]
    self.offset = data[2]
    self.flip = False
    self.animation_list = self.load_images(sprite_sheet, animation_steps)
    self.action = 0#0:idle #1:run #2:jump #3:attack1 #4: attack2 #5:hit #6:death
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
    self.jumpcooldown=0
    self.damage= 20
    self.interact=False
    self.xloc=x

    
  

  def load_images(self, sprite_sheet, animation_steps):
    #extract images from spritesheet
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

    #get keypresses
    key = pygame.key.get_pressed()


    if self.alive == True and round_over == False:
        #SAMURAI CONTROLS  
      if self.name == 3:
        speed = 10
        #movement
      if key[pygame.K_a]:
          dx = -SPEED
          self.running = True
          self.flip = True
      if key[pygame.K_d]:
          dx = SPEED
          self.running = True
          self.flip = False
        #jump
      if key[pygame.K_w] and self.jump == False and self.jumpcooldown == 0:
          self.vel_y = -30
          self.jump = True
          self.mana-=5

        #attack
      if key[pygame.K_p]:
          if key[pygame.K_p] and self.attackindex==1 and self.attack_cooldown==0 :
            self.attack(target)
            self.attack_type=1
            self.attack_cooldown=24
          if key[pygame.K_p] and self.attackindex==2 and self.attack_cooldown==0 :
            self.attack(target)
            self.attack_type=2
            self.attack_cooldown=24
      if self.action == 3 and self.frame_index>=5:
          self.attackindex=2
      elif self.action==4 and self.frame_index>=5:
          self.attackindex=1

      if key[pygame.K_a] or key[pygame.K_d]:
        if key[pygame.K_LSHIFT]: 
          if self.flip==True and self.mana > 10:
            dx-=20
            self.mana-=2

          elif self.flip==False:
            dx+=20
            self.mana-=2

      if key[pygame.K_e]:
        self.interact=True

      elif self.interact==True:
         self.interact= False



    #apply gravity
    self.vel_y += GRAVITY
    dy += self.vel_y

    #ensure player stays on screen
    if self.rect.left + dx < 0:
      dx = -self.rect.left
    if self.rect.right + dx > screen_width:
      dx = screen_width - self.rect.right
    if self.rect.bottom + dy > screen_height - 110:
      self.vel_y = 0
      self.jump = False
      dy = screen_height - 110 - self.rect.bottom

    #ensure players face each other 

    #apply attack cooldown
    if self.attack_cooldown > 0:
      self.attack_cooldown -= 1

    if self.jumpcooldown > 0:
      self.jumpcooldown -= 1

    #update player position
    self.rect.x += dx
    self.rect.y += dy


  #handle animation updates
  def update(self):
    #check what action the player is performing
    #stamina_regen
    if self.health > 100:
      self.health = 100
    if self.mana < 99.9:
      self.mana += .5
    if self.mana < 0:
      self.mana=0
    if self.health <= 0:
      self.health = 0
      self.alive = False
      self.update_action(6)#6:death
    elif self.hit == True:
      self.update_action(5)#5:hit
    elif self.attacking == True:
      if self.attack_type == 1:
        self.update_action(3)#3:attack1
      elif self.attack_type == 2:
        self.update_action(4)#4:attack2
    elif self.jump == True:
      self.update_action(2)#2:jump
      self.jumpcooldown=15
    elif self.running == True:
      self.update_action(1)#1:run
    else:
      self.update_action(0)#0:idle

    animation_cooldown = 50

    #update image
    self.image = self.animation_list[self.action][self.frame_index]

    #para di maulit sound
    if self.attacking and self.frame_index == 0 and self.attack_cooldown == 0:
      self.attack_sound.play()
      

    #check if enough time has passed since the last update
    if pygame.time.get_ticks() - self.update_time > animation_cooldown:
      self.frame_index += 1
      self.update_time = pygame.time.get_ticks()
    #check if the animation has finished
    if self.frame_index >= len(self.animation_list[self.action]):
      #if the player is dead then end the animation
      if self.alive == False:
        self.frame_index = len(self.animation_list[self.action]) - 1
      else:
        self.frame_index = 0

        #check if an attack was executed
        if self.action == 3 or self.action == 4:
          self.attacking = False
          self.attack_cooldown = 30


        #check if damage was taken
        if self.action == 5:
          self.hit = False
          #if the player was in the middle of an attack, then the attack is stopped
          self.attacking = False
          self.attack_cooldown = 20
    

  def attack(self, target):
    if self.attack_cooldown == 0 and self.mana > 20:
      #minus stamina every attack
      self.mana -= 15
      #execute attack
      self.attacking = True
      self.attack_sound.play()
      attacking_rect = pygame.Rect(self.rect.centerx - (6 * self.rect.width * self.flip), self.rect.y, 6 * self.rect.width, self.rect.height)
      if attacking_rect.colliderect(target.rect):
        target.health -= self.damage
        print("Goblin HP " + str(target.health))
        target.hit = True



  def update_action(self, new_action):
    #check if the new action is different to the previous one
    if new_action != self.action:
      self.action = new_action
      #update the animation settings
      self.frame_index = 0
      self.update_time = pygame.time.get_ticks()

  def draw(self, surface):
    img = pygame.transform.flip(self.image, self.flip, False)
    surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))


  #------------------------------------------------------------------------

  def draw_character_rect(self, surface):
          pygame.draw.rect(surface, (0, 0, 255), self.rect, 2)
          
  def draw_attacking_rect(self, surface):
          attacking_rect = pygame.Rect(self.rect.centerx - (4.7 * self.rect.width * self.flip),
                                       self.rect.y, 4.6 * self.rect.width, self.rect.height)
          pygame.draw.rect(surface, (255, 0, 0), attacking_rect, 2)

  #------------------------------------------------------------------------  

    
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
    def __init__(self, name, x, y, flip, data, sprite_sheet, animation_steps, sound):
        super().__init__(name, x, y, flip, data, sprite_sheet, animation_steps, sound)
        self.flip= True

#Goblin AI
class Monster(Character):
    def __init__(self, name, x, y, flip, data, sprite_sheet, animation_steps, sound):
        super().__init__(name, x, y, flip, data, sprite_sheet, animation_steps, sound)
        self.flip= True
        self.alive= True
        self.damagetoken=1



    def move(self, screen_width, screen_height, surface, target, round_over,xpos):
      SPEED = 4
      GRAVITY = 2
      dx = 0
      dy = 0
      self.running = False
      self.attack_type = 0
      self.xpos= xpos
      self.damage = 3

      if self.alive == True and self.attacking==False and round_over==False and self.rect.x-200 >= self.xpos:
          dx = -SPEED
          self.running = True
          self.flip= True

      if self.rect.x - self.xpos < 300 and self.attack_cooldown== 0 and self.flip==True:
            self.attack(target)
            self.attack_type=1
          

      if self.alive == True and round_over==False and self.attacking==False and self.rect.x+200 <= self.xpos:
          dx = SPEED
          self.running = True
          self.flip=False 
          
      if self.rect.x - self.xpos > -300 and self.attack_cooldown== 0 and self.flip== False:
            self.attack(target)
            self.attack_type=1


      #apply attack cooldown
      if self.attack_cooldown > 5:
        self.attack_cooldown -= 10
      
      self.rect.x += dx
      self.rect.y += dy
          

      #handle animation updates
      #iba yung self.action ng monster kasi mas maliit sheet 1atk 2death 3idle 4run 5hit
    def update(self):
        #check what action the player is performing
        if self.health <= 0:
          self.health = 0
          self.alive = False
          self.update_action(1)
        elif self.hit == True:
          self.update_action(4)
        elif self.attacking == True:
            
          if self.attack_type == 1:
            self.update_action(0)#
          elif self.attack_type == 2:
            self.update_action(0)
        elif self.running == True:
          self.update_action(3)
        else:
          self.update_action(2)#

        animation_cooldown = 50

        #update image
        self.image = self.animation_list[self.action][self.frame_index]

        #para di maulit sound
        

        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
          self.frame_index += 1
          self.update_time = pygame.time.get_ticks()
        #check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
          #if the player is dead then end the animation
          if self.alive == False:
            self.frame_index = len(self.animation_list[self.action]) - 1
          else:
            self.frame_index = 0

            #check if an attack was executed
            if self.action == 0:
              self.attacking = False
              self.attack_cooldown = 360


              #check if damage was taken
            if self.action == 4:
              self.hit = False
              #if the player was in the middle of an attack, then the attack is stopped
              self.attacking = False
              self.attack_cooldown = 20

       


    def attack(self, target):
      attacking_rect = pygame.Rect(self.rect.centerx - (3 * self.rect.width * self.flip),
                                     self.rect.y*1.15, 3 * self.rect.width, self.rect.height*.5) 

      if self.attack_cooldown == 0 and self.alive == True and target.health>0 and self.attacking==False:
      #execute attack
        self.attacking = True
        self.attack_sound.play()
                
        
        
        
      # Check if the current frame is within the damage frames
      if self.attacking==True:
        hit=attacking_rect.colliderect(target.rect)
        if hit==True and self.frame_index==6 and self.damagetoken==1:
          self.damagetoken=0
          target.health -= self.damage
          print("Main MC HP " + str(target.health))
          target.hit = False
        elif self.damagetoken==0:
          self.damagetoken=1  

        
#Debug tools
    def draw_attacking_rect(self, surface):
        attacking_rect = pygame.Rect(self.rect.centerx - (3 * self.rect.width * self.flip),
                                     self.rect.y*1.15, 3 * self.rect.width, self.rect.height*.5)
        pygame.draw.rect(surface, (255, 0, 0), attacking_rect, 2)  

    def draw_goblin_rect(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), self.rect, 2)
        

          

class Monster_Skeleton(Monster):
    def __init__(self, name, x, y, flip, data, sprite_sheet, animation_steps, sound):
        super().__init__(name, x, y, flip, data, sprite_sheet, animation_steps, sound)
        self.flip= True
        self.alive= True
        self.damagetoken=1
        self.truehit=False
        self.falsehit=False
        self.regenrate=0.1

    def move(self, screen_width, screen_height, surface, target, round_over,xpos):
      SPEED = 2
      GRAVITY = 2
      dx = 0
      dy = 0
      self.running = False
      self.attack_type = 0
      self.xpos= xpos
      self.damage = 3

      if self.alive == True and self.attacking==False and round_over==False and self.rect.x-200 >= self.xpos:
          dx = -SPEED
          self.running = True
          self.flip= True

      if self.rect.x - self.xpos < 300 and self.attack_cooldown== 0 and self.flip==True:
            self.attack(target)
            self.attack_type=1
          

      if self.alive == True and round_over==False and self.attacking==False and self.rect.x+200 <= self.xpos:
          dx = SPEED
          self.running = True
          self.flip=False 
          
      if self.rect.x - self.xpos > -300 and self.attack_cooldown== 0 and self.flip== False:
            self.attack(target)
            self.attack_type=1


      #apply attack cooldown
      if self.attack_cooldown > 5:
        self.attack_cooldown -= 10
      
      self.rect.x += dx
      self.rect.y += dy
      self.health+=self.regenrate
          

      #handle animation updates
      #iba yung self.action ng monster kasi mas maliit sheet 0atk 1death 2idle 3run 4hit 5block
    def update(self):
        #check what action the player is performing
        if self.health > 100:
          self.health = 100
        if self.health <= 0:
          self.regenrate=0
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
            self.update_action(0)#
          elif self.attack_type == 2:
            self.update_action(0)
        elif self.running == True:
          self.update_action(3)
        else:
          self.update_action(2)#

        animation_cooldown = 50

        #update image
        self.image = self.animation_list[self.action][self.frame_index]

        #para di maulit sound
        

        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
          self.frame_index += 1
          self.update_time = pygame.time.get_ticks()
        #check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
          #if the player is dead then end the animation
          if self.alive == False:
            self.frame_index = len(self.animation_list[self.action]) - 1
          else:
            self.frame_index = 0

            #check if an attack was executed
            if self.action == 0:
              self.attacking = False
              self.attack_cooldown = 360


              #check if damage was taken
            if self.action == 4:
              self.truehit = False
              #if the player was in the middle of an attack, then the attack is stopped
              self.attacking = False
              self.attack_cooldown = 20

            if self.action == 5:
              self.falsehit = False
              self.attacking = False
              #if the player was in the middle of an attack, then the attack is stopped
              self.health+=20




        print(self.hit)
        #print(self.truehit)
              

     
            
             