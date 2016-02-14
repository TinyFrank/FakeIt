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
		self.color = color
		self.quality = quality
		self.q_forbid=[]
		self.m_forbid=[]
		self.c_forbid=[]
		#list of possible loot qualities
		self.qualities = (	('ruined ',0.2), 
							('busted ',0.4),
							('scratched ',0.6),
							('used ',0.75), 
							('ordinary ',0.9),
							('new ',1.0),
							('quality ',1.25), 
							('top notch ',1.5), 
							('special edition ',2.0), 
							('luxury ',5.0))
		#list of possible 'hard' metals, for cooking and what have you					
		self.ferros = ( 	('tin ',0.6,(172,182,192)), 
							('copper ',0.7,(255,120,0)),
							('brass ',0.8,(218,165,32)), 
							('iron ',0.9,(128,128,128)),		
							('steel ',1.0,(192,192,192)),
							('carbon steel ',1.5,(108,118,128)),
							('stainless steel ',3.0,(176,196,222)))
		#list of available paint colours					
		self.colors = (		('red ',(200,30,30)), 				
							('blue ',(30,30,200)),				
							('olive ',(128,128,0)), 			
							('khaki ',(240,230,140)),
							('dark green ',(0,100,0)),
							('lime green ',(50,205,50)),
							('teal ',(0,128,128)),
							('indigo ',(75,0,130)),
							('purple ',(128,0,128)), 
							('deep pink ',(255,20,147)),
							('pink ', (255,192,203)), 
							('beige ',(245,245,220)),
							('orange ', (255,165,0)), 
							('yellow ',(255,255,0)) )
		
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
		
		#num of colour layers in 'M' palette
		self.layers = (len(self.image_col.get_palette())) 
		
		#if the quality is any worse than 'new' create some 'dents'
		if self.q_num < 5:
			self.dents = (int(self.layers/5) * self.q_num)+1
			
		#otherwise specify that there are no dents
		else:
			self.dents = 0
		
		#apply the dents by make paint fragments transparent	
		for i in range(0,self.layers):
			if self.dents:
				self.image_col.set_palette_at(i,self.mat[2])
				self.dents -= 1
			else:
				self.image_col.set_palette_at(i,self.color[1])
		
		#pick an alpha between 0 and 255 based on quality number		
		self.alpha = (self.q_num * 51)-25
		if self.alpha > 255:
			self.alpha = 255
		if self.alpha < 0:
			self.alpha = 0
		self.alpha = 255 - self.alpha
		
	def blit_alpha(self,target, source, location, opacity):
		"""
		workaround to blit a pixel-alpha containing surface at an
		opacity other than 100
		"""
		self.x = location[0]
		self.y = location[1]
		self.temp = pygame.Surface((source.get_width(), source.get_height())).convert()
		self.temp.blit(target, (-self.x, -self.y))
		self.temp.blit(source, (0, 0))
		self.temp.set_alpha(opacity)        
		target.blit(self.temp, location)	
        
	def blitme(self):
		"""Draw the ship at it's current location."""
		self.screen.blit(self.image_col,self.rect) #Color (Paintjob)
		self.screen.blit(self.image_line,self.rect) #Line art
		self.blit_alpha(self.screen,self.image_dirt,self.rect,self.alpha)

class Barbecue(Loot):
	def __init__(self,settings,screen,weight,value, color=None ,quality = None):
		super().__init__(settings, screen, weight, value, color, quality)
		self.q_forbid=[]
		self.m_forbid=[]
		self.c_forbid=[]
		
		#if no quality was specified, select one randomly
		if self.quality == None:
			while True:
				self.q_num = randint(0,len(self.qualities)-1)
				if self.q_num not in self.q_forbid:
					self.quality = self.qualities[self.q_num]
					break
					
		#otherwise, save quality to q_num and reload quality from list			
		else:
			self.q_num = self.quality
			self.quality = self.qualities[self.q_num]
					
		#decide material
		self.mat = self.ferros[randint(0,len(self.ferros)-1)]
		
		#decide color
		if not self.color:
			self.color = self.colors[randint(0,len(self.colors)-1)]
		
		#define trim as a material
		self.trim = self.mat
		
		#iterate over trim until it is a different material than mat
		while self.trim == self.mat:
			self.trim = self.ferros[randint(0,len(self.ferros)-1)]
		
		"""
		self.parts contains the 'parts' into which the loot is broken
		down. each has a name, a material form factor, and quantity, 
		and a factor relating to how mcuh 'material' it contribues to 
		the loot overall.
		
		As an example, there are 3 legs that contribute 2 to the overall
		mass, while the 10 screws only contribute 1.
		"""
		self.parts = [ 	["legs ","rod ",3,2],
						["grill ","mesh ",1,3],
						["lid ","sheet ",1,4],
						["base ","sheet ",1,4],
						["screws ","chunk ",10,1] ]	
						
		self.val_x = 0
		self.val_normal = 0
		
		#for each part...
		for i in self.parts:
			#20% change to change the material to trim material
			if randint(0,10) < 8:
				i.append(self.mat)
			else:
				i.append(self.trim)
			self.val_x += i[3]*i[4][1]
			self.val_normal += i[3]
		
		#create a final factor by taking the weighed average of the parts
		self.val_x /= self.val_normal
		
		#set value
		self.value *= 20 #cost of a 'new, steel' bbq IRL, for balancing
		self.value *= round(self.quality[1]*self.mat[1],2)
		self.value *= round(self.val_x,2)
			
		#compose name
		self.name = self.quality[0].title() + self.mat[0].title() + 'Barbecue '
		self.name = self.name + 'with ' + self.color[0].title() + 'paint.'
		
		#compose descriptive string for Loot PIP
		self.desc = "Material:\t" + self.mat[0].upper()
		self.desc += "\nTrim:\t\t" + self.trim[0].upper()
		self.desc += "\nQuality:\t" + self.quality[0].upper()
		self.desc += "\nColor:\t\t" + self.color[0].upper()
		self.desc += "\nValue:\t\t$" + str(self.value).upper()
		self.desc += "\nWeight:\t\t" + str(self.weight).upper() + 'kg'
		print(self.desc)		
		#compose image from source and alter based on qual/mat/color
		self.set_images('bbq_D.png','bbq_L.png','bbq_M.png')
		
		##debug terminal print
		#print('\n' + self.name + ' worth ' + str(round(self.value,2)))
		#for i in self.parts:
			#print('\t..contains ' + str(i[2]) + ' ' + i[0], end = '')
			#print('made of ' + i[4][0] + i[1] + '. :' + str(self.alpha))
		
		
		
		#create rects
		self.rect = self.image_line.get_rect()
		self.collide_rect = self.image_line.get_rect()
		self.screen_rect = self.screen.get_rect()
		self.collide_rect.width *= .8		
		self.collide_rect.height *= .8
		
		
	def breakdown(self,inv):
		pass
