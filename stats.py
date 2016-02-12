class Stats():
	"""Track stats for Fake It Til You Make It"""
	
	def __init__(self, settings):
		"""Initialize statistics."""
		self.settings = settings
		self.reset_stats()
		
		#High score should never be reset
		self.high_score = 0
	
		#Start alien invasion in an active state
		self.game_active = False
		
		#When to display and activate title card and menu
		self.menu = -self.game_active
	
	def reset_stats(self):
		"""Initialize statistics that can change during the game"""
		self.score = 0
		self.level = 1
