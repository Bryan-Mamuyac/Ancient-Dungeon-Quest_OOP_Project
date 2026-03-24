import pygame


class Fireball():

	def __init__(self,x,y,flip,data,sprite_sheet,animation_steps):

	    self.size = data[0]
	    self.image_scale = data[1]
	    self.offset = data[2]
	    self.flip = False
	    self.animation_list = self.load_images(sprite_sheet, animation_steps)
	    self.action = 0
	    self.frame_index = 0
	    self.image = self.animation_list[self.action][self.frame_index]
	    self.update_time = pygame.time.get_ticks()
	    self.rect = pygame.Rect((x, y, 80, 180))
	    self.running = False
	    self.alive = True
	    self.damage= 15

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
		SPEED=10
		dx=15

		if self.alive and round_over==False:
			if self.running:
				self.update_action(0)
			if self.rect.colliderect(target.rect):
				self.update_action(1)
				target.health-=self.damage

		self.rect.x += dx


		

	def update(self,target):

		if self.running:
			self.update_action(1)
		if self.rect.colliderect(target.rect):
			self.update_action(0)
			target.health-=self.damage
			hit=True
		if hit and self.frame_index==6:
			self.alive=False

		animation_cooldown = 50

	    
		self.image = self.animation_list[self.action][self.frame_index]

	      

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

	def update_action(self, new_action):
    #check if the new action is different to the previous one
	    if new_action != self.action:
	      self.action = new_action
	      #update the animation settings
	      self.frame_index = 0
	      self.update_time = pygame.time.get_ticks()

	def draw(self, surface):
		img = pygame.transform.flip(self.image, self.flip, False)
		if self.alive:
			surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
