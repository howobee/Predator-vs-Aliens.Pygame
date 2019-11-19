class Settings():
	""" Класс для хранения настроек игры"""
	def __init__(self):	
		"""инициализирует настройки игры"""
		self.screen_wight = 900
		self.screen_height = 600
		self.bg_color = (255, 255, 255)
		#Настройка корабля
		
		self.ship_limit = 3
		#Темп ускорения игры
		self.speedup_scale = 1.1
		
		self.initialize_dynamic_settings()
		#Параметр пули
		
		self.bullet_width = 3
		self.bullet_height = 8
		self.bullet_color = 200, 0, 100
		self.bullet_allowed = 3
		# Настройка пришельца 
		
		self.fleet_drop_speed = 10
		#fleet_direction = 1 обозначает движение вправо, а -1 влево
		self.fleet_direction = 1
	def initialize_dynamic_settings(self):
		"""Инициализирует настройки изменяющиеся в ходе игры."""
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 5
		self.alien_speed_factor = 1
		#fleet_direction = 1 обозначает движение вправо, а -1 влево
		self.fleet_direction = 1
	def increase_speed(self):
		"""Увеличивает настройки скорости."""
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale 
		self.alien_speed_factor *= self.speedup_scale
		