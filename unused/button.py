import pygame
import main 


class Button():
	def __init__(self,x,y,image,scale,name):
		width= image.get_width()
		height=image.get_height()
		self.image = pygame.transform.scale(image,(int(width*scale),(int(height*scale))))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x,y)
		self.active=False
		self.x=x
		self.y=y
		self.name=name


	def draw_text(self,text,color,x,y):

    		font=pygame.font.Font("assets/fonts/ancient.ttf", 25)
    		img = font.render(text, True, color)
    		screen.blit(img, (x, y))

	def draw(self):
		

		pos= pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):

			self.draw_text(self.name,WHITE,self.x+70,self.y+203)

			if pygame.mouse.get_pressed()[0]== 1 and self.clicked == False:
				self.clicked= True
				self.active = True
				main.toggleSelect()

		if pygame.mouse.get_pressed()[0]== 0:
			self.clicked = False
			


		screen.blit(self.image,(self.rect.x,self.rect.y))
		print(self.active)

		