from random import randint
import pygame
from pygame.sprite import Sprite

class Loot(Sprite):
	def __init__(self,settings,screen,weight,value,quality = randint(0,9)):
		super(Loot, self).__init__()
		self.settings = settings
		self.screen = screen
		self.weight = weight
		self.value = value
		self.quality = quality
		self.qualities = (	'ruined', 'busted', 'scratched', 'used, ordinary', 
					'new', 'quality', 'top notch', 
					'special edition', 'luxury')
		
	def blitme(self):
		"""Draw the ship at it's current location."""
		self.screen.blit(self.image,self.rect)
		self.screen.blit(self.image_line,self.rect)

class Barbecue(Loot):
	def __init__(self,settings,screen,weight,value, quality = randint(0,9)):
		super().__init__(settings, screen, weight, value, quality)
		
		self.qname = self.qualities[quality]
		self.mat = 'Steel'
		self.name = str(self.qname).title() + ' ' + str(self.mat) + ' Barbecue'
		self.image_dirt = pygame.image.load('barbecue_D.png')
		self.image_line = pygame.image.load('barbecue_L.png')
		self.image = pygame.image.load('barbecue.png')
		
		self.rect = self.image.get_rect()
		self.collide_rect = self.image.get_rect()
		self.screen_rect = self.screen.get_rect()
		self.collide_rect.width *= .8		
		self.collide_rect.height *= .8
		
		self.parts = { 	("legs","rod","metal"),
						("grill","mesh","metal"),
						("lid","sheet","metal"),
						("base","sheet","metal"),
						("screws","chunk","metal") }
		
	def breakdown(self,inv):
		pass
		
