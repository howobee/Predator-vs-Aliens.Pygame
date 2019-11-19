class GameStats():
	"""Отслеживание статистики для игры Predator vs Aliens"""
	
	def __init__(self, ai_settings):
		"""Инициализирует статистику игры."""
		self.ai_settings = ai_settings
		self.reset_stats()
		self.game_active = True
	
		#Игра запускается в неактивном состоянии
		self.game_active = False
	
	def reset_stats(self):
		"""Инициализирует статистику изменяющиеся в ходе игры."""
		self.ships_left = self.ai_settings.ship_limit
	