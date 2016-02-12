"""
Fake It Til You Make It
"""
import sys
import pygame
from pygame.sprite import Group
import json
from button import Button
from settings import Settings
import display
import functions as gf
from stats import Stats
from player import Player

def run():
	#Initialize game, settings and create a screen object
	pygame.init()	
	settings = Settings()
	screen_setup = display.build(settings)
	screen = screen_setup[0]
	pygame.display.set_caption("Fake It Til You Make It")
	
	#Change screen dims to match fullscreen dims
	settings.screen_width = screen_setup[1]
	settings.screen_height = screen_setup[2]
	
	#Make Main Menu
	buttons = []
	play_button = Button(settings, screen, "NEW GAME",
		settings.screen_width/2-100, 500,
		300,75,(0,0,0),None)
	quit_button = Button(settings, screen, "QUIT",
		settings.screen_width/2-100, 600,
		300,75,(0,0,0),None)
	buttons.append(play_button)
	buttons.append(quit_button)
	
	#Make Ingame Menu
	inv_button = Button(settings, screen, "INVENTORY",
		settings.screen_width*.2-100, 100,
		300,75,(0,0,0),None)
	craft_button = Button(settings, screen, "CRAFT",
		settings.screen_width*.35-100, 100,
		300,75,(0,0,0),None)
	build_button = Button(settings, screen, "BUILD",
		settings.screen_width/2-100, 100,
		300,75,(0,0,0),None)
	character_button = Button(settings, screen, "CHARACTER",
		settings.screen_width*.65-100, 100,
		300,75,(0,0,0),None)
	menu_button = Button(settings, screen, "MENU",
		settings.screen_width*.8-100, 100,
		300,75,(0,0,0),None)
	buttons.append(inv_button)
	buttons.append(craft_button)
	buttons.append(build_button)
	buttons.append(character_button)
	buttons.append(menu_button)
	
	#Create a stats instance
	stats = Stats(settings)
	
	#Create item groups
	player = Player(settings, screen)
	furniture = Group()
	items = Group()
	loot = Group()
	customers = Group()
	
	#Create clock to stabilize framerate
	clock = pygame.time.Clock()
	
	#Initialize Global Variables
	day = 1
	hour = 6
	minute = 0
	
	while True:
		clock.tick(100)
		gf.check_events(settings, screen, stats, buttons)
		gf.update_screen(settings,screen, stats, buttons, player)
run()
	
