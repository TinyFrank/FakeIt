from random import randint
import pygame
from pygame.sprite import Sprite

class Loot(Sprite):
	def __init__(self,settings,screen,weight,value,color,quality):
		super(Loot, self).__init__()
		self.settings = settings
		self.screen = screen
		self.weight = weight
		self.value = value
		self.quality = quality
		#list of possible loot qualities
		self.qualities = (	('ruined',0.2), ('busted',0.4),
							('scratched',0.6),('used',0.75), 
							('ordinary',0.9),('new',1.0),
							('quality',1.25), ('top notch',1.5), 
							('special edition',2.0), ('luxury',10.0))
		#list of possible 'hard' metals, for cooking and what have you					
		self.ferros = ( 	('tin',0.7,(172,182,192)), 
							('brass',0.8,(218,165,32)), 
							('iron',0.9,(128,128,128)),		
							('steel',1.0,(192,192,192)),
							('carbon steel',1.5,(108,118,128)),
							('stainless steel',3.0,(176,196,222)))
		#list of available paint colours					
		self.colors = (		('red',(200,30,30)), ('blue',(30,30,200)))
		
	def set_images(self,D,L,M):
		"""
		Loads in the three images(Dirt, Line and Material) that are
		used to generate the procedural graphic.
		The material layer is full of coloured fragments and is used
		twice; once in the bottom layer for MAT and again in the second
		from top layer for COL. Each time it's colours are changed to 
		match that of the chosen paint and material. In the case of the
		paint, some of the fragments are made transparent to reveal
		the material layer below.
		"""
		self.image_dirt = pygame.image.load(D)
		self.image_dirt.convert_alpha()
		self.image_line = pygame.image.load(L)
		self.image_line.convert_alpha()
		self.image_col = pygame.image.load(M)
		self.image_col.convert_alpha()
		self.image_mat = pygame.image.load(M)
		self.image_mat.convert_alpha()
		pal = self.image_col.get_palette()
		self.image_col.set_palette_at(1,self.color[1])
		self.alpha = self.quality * 51
		if self.alpha > 255:
			self.alpha = 255
		self.image_col.set_alpha(self.alpha)
		self.image_mat.set_palette_at(1,self.mat[2])
		
	def blitme(self):
		"""Draw the ship at it's current location."""
		self.screen.blit(self.image_mat,self.rect) #Material
		self.screen.blit(self.image_dirt,self.rect) #Dirt and Dents
		self.screen.blit(self.image_col,self.rect) #Color (Paintjob)
		self.screen.blit(self.image_line,self.rect) #Line art

class Barbecue(Loot):
	def __init__(self,settings,screen,weight,value, color=None ,quality = None):
		super().__init__(settings, screen, weight, value, color, quality)
		
		#if no quality was specified, select one randomly
		if self.quality == None:
			self.quality = randint(0,len(self.qualities)-1)
		
		#decide quality, material, value and color
		self.qname = self.qualities[self.quality]
		self.mat = self.ferros[randint(0,len(self.ferros)-1)]
		self.value *= self.qname[1]*self.mat[1]
		self.color = self.colors[randint(0,len(self.colors)-1)]
		
		#compose name
		self.name = self.qname[0].title() + ' ' + self.mat[0].title() + ' Barbecue'
		self.name = self.name + ' with ' + self.color[0].title() + ' paint.'
		
		#compose image from source and alter based on qual/mat/color
		self.set_images('bbq_D.png','bbq_L.png','bbq_M.png')
		self.rect = self.image_line.get_rect()
		self.collide_rect = self.image_line.get_rect()
		self.screen_rect = self.screen.get_rect()
		self.collide_rect.width *= .8		
		self.collide_rect.height *= .8
		
		#define component parts for disassembly
		self.parts = { 	("legs","rod","metal"),
						("grill","mesh","metal"),
						("lid","sheet","metal"),
						("base","sheet","metal"),
						("screws","chunk","metal") }
		
	def breakdown(self,inv):
		pass
		
