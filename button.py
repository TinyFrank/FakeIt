import pygame.font

class Button():
	
	def __init__(self, settings, screen, msg,x,y,w,h,colour,image):
		"""Initialize button attributes"""
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.settings = settings
		
		#set the dimensions and properties of the button
		self.width, self.height = w, h
		self.button_colour = colour
		self.text_colour = (255,255,255)
		self.font = pygame.font.Font('cour.ttf', 48)
								
		#Build the button's rect object and position it
		self.rect = pygame.Rect(x,y,self.width,self.height)
		
		#The button message needs to be prepped only once
		self.prep_msg(msg)
	
	def prep_msg(self, msg):
		"""Turn msg into a rendered image and center text on the button"""
		self.msg_image = self.font.render(msg, True, self.text_colour, 
			self.button_colour)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center

	def draw_button(self):
		#Draw blank button and then draw message
		self.screen.fill(self.button_colour, self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)

