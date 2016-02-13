import sys
from time import sleep
from random import randint
import json
from player import Player
from libs import *
import pygame

def check_keydown_events(event, settings, screen, stats, loots):
	"""Respond to keypresses"""
	if event.key == pygame.K_q:
		sys.exit()
	elif event.key == pygame.K_c:
		barbecue = Barbecue(settings, screen, 2.0, 200) 
		x = randint(100,screen.get_width()-100)
		y = randint(300,screen.get_height()-100)
		barbecue.rect.x = x - (barbecue.rect.width/2)
		barbecue.rect.y = y - (barbecue.rect.height/2)
		print('You found a ' + barbecue.name + ' which is worth ' + str(round(barbecue.value,2)))
		loots.add(barbecue)
	elif event.key == pygame.K_d:
		for i in loots:
			print(i.name)
		
#def check_keyup_events(event,settings, screen, stats):
	#"""Respond to keyreleases"""		

def check_buttons(settings, screen, stats, buttons, mouse_pos):
	"""Start new game when player clicks Play"""
	contact = False
	clicked = 0
	for button in range(0,len(buttons)):
		contact = buttons[button].rect.collidepoint(mouse_pos[0], mouse_pos[1])
		if contact:
			clicked = button +1
		
	if clicked == 1 and not stats.game_active:
				
		##Reset the game stats
		#stats.reset_stats()
		stats.game_active=True
		## Reset the scoreboard images.
		#sb.prep_score()
		#sb.prep_high_score()
		#sb.prep_level()
		#sb.prep_ships()
	
	if clicked == 2 and not stats.game_active:
		sys.exit()
		
	if clicked == 7 and stats.game_active:
		stats.game_active=False
								
def check_events(settings, screen, stats, buttons, loots):
	"""Respond to keyboard and mouse events"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, settings, screen, stats, loots)		
		#elif event.type == pygame.KEYUP:
			#check_keyup_events(event, settings, screen, stats)	
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_pos = pygame.mouse.get_pos()
			check_buttons(settings, screen, stats, buttons, mouse_pos)

def update_screen(settings, screen, stats, buttons, player, loots):
	"""Update images on the screen and flip to the new screen"""

	#Redraw the screen during each pass through the loop
	screen.fill(settings.bg_colour)
	
	#Draw the menu button if the game is inactive
	if not stats.game_active:
		for button in range(0,2):
			buttons[button].draw_button()
	
	if stats.game_active:
		for i in loots:
			i.blitme()
		player.blitme()
		for button in range(2,7):
			buttons[button].draw_button()
			
	#Make the most recently drawn screen visible
	pygame.display.flip()

