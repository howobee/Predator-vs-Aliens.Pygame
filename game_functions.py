import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
pygame.init()



def check_keydown_events(event, ai_settings, screen, ship, bullets):
	"""Реагирует на нажатие клавиш."""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	
	elif event.key == pygame.K_SPACE:
		# Создание новой пули и включение ее в группу bullets
		fire_bullet(ai_settings, screen, ship, bullets)
	elif  event.key == pygame.K_q or pygame.K_ESCAPE:		
		
		sys.exit()
def check_keyup_events(event, ai_settings, screen, ship):
	"""Реагирует на отпускание клавиш."""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
	

def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets):
	"""Обрабатываем нажатия клавиш и событий мыши"""
	for event in pygame.event.get():					
			
		if event.type == pygame.QUIT:
			sys.exit()
		
		elif event.type == pygame.KEYDOWN:
						
			check_keydown_events(event,  ai_settings, screen, ship, bullets )
			
			
			
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, )
		
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ai_settings, screen, ship, )	
		
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x , mouse_y = pygame.mouse.get_pos()
						
			check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y)
	
def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y):
	"""Запускает игру при нажатии кнопки PLAY"""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		# Сброс игровой статистики.
		stats.reset_stats()		
		stats.game_active = True
		# Сброс игровых настроек.
		ai_settings.initialize_dynamic_settings()
		# Очистка списков пришельцев и пуль.
		aliens.empty()
		bullets.empty()
		
		# Создание нового флота и размещение корабля в центре.
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		# Указатель мыши скрывается.
		pygame.mouse.set_visible(False)


def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button):
	""" Обновляет изображения на экране и отображает новый экран."""
	# При каждом проходе цикла перерисовывается экран.
	screen.fill(ai_settings.bg_color)
	#Все пули выводятся позади изображения корабля и пришельцев.
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	
	ship.blitme()
	
	aliens.draw(screen)
	
	
	# Кнопка PLAY отображается в том случае если игра не активна
	if not stats.game_active:
		play_button.draw_button()
	
	# Отображения последнего прорисованного экрана.
	pygame.display.flip()
	
def update_bullets(ai_settings, screen, ship, aliens, bullets):
	""" Обновляет позиции пуль и уничтожает старые пули"""
	#Удаление пуль вышедших за границу экрана
	for bullet in bullets.copy():
		if bullet.rect.bottom <=0:
			bullets.remove(bullet)
	check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)
		
	if len(aliens) == 0:
		# Уничтожение существующих пуль и создания нового флота и повышения темпа игры
		bullets.empty()
		ai_settings.increase_speed()
		create_fleet(ai_settings, screen, ship, aliens)

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
	"""Обработка коллизий пуль с пришельцами. """
	#Удаление пуль и пришельцев
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	

def fire_bullet(ai_settings, screen, ship, bullets):
	"""Выпускает пулю если максимум еще не достигнут"""
	if len(bullets) < ai_settings.bullet_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)
			
def get_number_aliens_x(ai_settings, alien_width):
	"""Вычисляем количество пришельцев в ряду."""
	available_space_x = ai_settings.screen_wight - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x
	
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""Создает пришельца и размешает его в ряду."""
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
	"""Создает флот пришельцев."""
	# Создания пришельца и вычисления количества пришельцев в ряду
	# Интервал между соседними пришельцами равен одной ширине пришельца.
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
	
	
	
	
	#Создания первого ряда пришельцев
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			#Создание пришельца и размешения его в ряду
			create_alien(ai_settings, screen, aliens, alien_number, row_number)
		 
def get_number_rows(ai_settings, ship_height, alien_height):
	"""Определяет количество рядов помещаюшихся на экране."""
	available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (3 * alien_height ))
	return number_rows
	
def check_fleet_edges(ai_settings, aliens):
	"""Реагирует на достижения пришельцем края экрана."""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break
			
def change_fleet_direction(ai_settings, aliens):
	"""Опускает весь флот и меняет направление флота."""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
	"""Обрабатывает столкновение  корабля с пришельцем."""
	if stats.ships_left > 0:
		# Уменьшения ships_left
		stats.ships_left -= 1
		
		# Очистка списков пришельцев и пуль.
		aliens.empty()
		bullets.empty()

		# Создания нового флота и размещение корабля в центре.
		create_fleet(ai_settings,  screen, ship, aliens)
		ship.center_ship()
	
		#пауза
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
	"""Обновляет позиции все пришельцев во флоте."""
	check_fleet_edges(ai_settings, aliens)
	#Проверка пришельцев добравшихся до нижнего края экрана
	check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)
	
	aliens.update()
	# Проверка коллизий "пришелец - корабль"
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
		
def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
	""" Пороверяет добрались ли пришельцы до нижнего края экрана."""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# Происходит то же что и столкновение с кораблем
			ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

		
		
	
	