import sys 
import pygame
from ship import Ship
from setting import Settings
from pygame.sprite import Group
import game_functions as gf
from alien import Alien
from game_stats import GameStats
from button import Button



def run_game():
	#Инициализирует игру и создает объект экрана.
	pygame.init()
	
	ai_settings = Settings()
	screen = pygame.display.set_mode(
	(ai_settings.screen_wight, ai_settings.screen_height))
	pygame.display.set_caption("Predator vs Aliens")
	pygame.display.set_icon(pygame.image.load("images/icon.png"))
	#Создание корабля
	ship = Ship( ai_settings, screen )
	
	# Создание группы для хранения пуль
	bullets = Group()
	
	#Создание пришельца и группы пришельцев
	aliens = Group()
	alien = Alien(ai_settings, screen)
	# Создания флота пришельцев
	gf.create_fleet(ai_settings, screen, ship, aliens)
	
	# Создания экземпляра для хранения игровой статистики
	stats = GameStats(ai_settings)
	# Создание кнопки Play.
	play_button = Button(ai_settings, screen, "PLAY")
# Запуск основного цикла игры.
	while True:
		#отслеживание событий клавиатуры и мыши
		gf.check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets)
		if stats.game_active:
		
			ship.update()
			bullets.update()
			gf.update_bullets(ai_settings, screen, ship, aliens, bullets)				
			gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
		gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button)
		
		
		
		

run_game()