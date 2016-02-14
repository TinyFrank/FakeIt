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
	
	#create variables for screen center
	scx = settings.screen_width/2
	scy = settings.screen_height/2
	#Make Main Menu
	buttons = []
	play_button = Button(settings, screen, "NEW GAME",
		scx-100, 500, 300,75,(0,0,0),None)
	quit_button = Button(settings, screen, "QUIT",
		scx-100, 600, 300,75,(0,0,0),None)
	buttons.append(play_button)
	buttons.append(quit_button)
	
	#Make Ingame Menu
	ig_buttons = []
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
	ig_buttons.append(inv_button)
	ig_buttons.append(craft_button)
	ig_buttons.append(build_button)
	ig_buttons.append(character_button)
	ig_buttons.append(menu_button)
	
	#Make Loot PIP menu
	lp_buttons = []
	lptake_button = Button(settings, screen, "TAKE",
		scx+25, scy-75, 200,50,(0,0,0),None,20)
	lpdesc_button = Button(settings, screen, "DESCRIBE",
		scx+25, scy+25, 200,50,(0,0,0),None,20)
	lp_window = Button(settings, screen, "",
		scx-250, scy-150, 500,300,(100,100,100),None)
	lp_loot_window = Button(settings, screen, "",
		scx-225, scy-125, 200,250,(180,180,180),None)
	lp_loot = Button(settings, screen, "",
		scx-215, scy-115, 180,230,(250,250,250),None)
	lp_buttons.append(lp_window)
	lp_buttons.append(lptake_button)
	lp_buttons.append(lpdesc_button)
	lp_buttons.append(lp_loot_window)
	lp_buttons.append(lp_loot)
	
	#Create a stats instance
	stats = Stats(settings)
	
	#Create item groups
	player = Player(settings, screen)
	furniture = Group()
	items = Group()
	loots = Group()
	customers = Group()
	
	#Create clock to stabilize framerate
	clock = pygame.time.Clock()
	
	#Initialize Global Variables
	day = 1
	hour = 6
	minute = 0
	
	while True:
		clock.tick(100)
		gf.check_events(settings, screen, stats, buttons, loots)
		gf.update_screen(	settings,screen, stats, buttons, ig_buttons, 
							lp_buttons, player, loots)
run()
	
