import sys
import time

import pygame

from Bullet import Bullet
from Settings import Settings
from Ship import Ship
from Invader import Invader
from GameStatistics import GameStats
from ScoreTable import ScoreTable
from Button import Button


class SpaceInvaders:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((
            self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Space Invaders")
        self.background_image = pygame.image.load('images/background.jpg')

        self.ship = Ship(self)

        # Группа для управления спрайтами
        self.bullets = pygame.sprite.Group()
        self.invaders = pygame.sprite.Group()
        self._create_armada()

        # Игровая статистика
        self.stats = GameStats(self)
        self.score_table = ScoreTable(self)

        self.play_button = Button(self, "Play")

    def run_game(self):
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_invaders()

            self._update_screen()

    # Создание флота
    def _create_armada(self):
        invader = Invader(self)
        invader_width, invader_height = invader.rect.size
        available_space_x = self.settings.screen_width - (2 * invader_width)
        numbers_of_invaders = available_space_x // (2 * invader_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * invader_height) - ship_height)
        numbers_rows = available_space_y // (2 * invader_height)

        for row_number in range(numbers_rows):
            for invader_number in range(numbers_of_invaders):
                self._create_invader(invader_number, row_number)

    # Создание пришельца
    def _create_invader(self, invader_number, row_number):
        invader = Invader(self)
        invader_width, invader_height = invader.rect.size
        invader.x = invader_width + 2 * invader_width * invader_number
        invader.rect.x = invader.x
        invader.rect.y = invader.rect.height + 2 * invader.rect.height * row_number
        self.invaders.add(invader)

    def _update_invaders(self):
        self._checks_armada_edges()
        self.invaders.update()

        # Если пришелец добрался до корабля - гг умер
        if pygame.sprite.spritecollideany(self.ship, self.invaders):
            self._ship_hit()
        # Если пришелец добрался до низа - гг умер
        self._check_invaders_bottom_collision()

    def _checks_armada_edges(self):
        for invader in self.invaders.sprites():
            if invader.check_edges():
                self._change_armada_direction()
                break

    def _change_armada_direction(self):
        for invader in self.invaders.sprites():
            invader.rect.y += self.settings.armada_drop_speed
        self.settings.armada_direction *= -1

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.score_table.prep_life()

            self.invaders.empty()
            self.bullets.empty()

            self._create_armada()
            self.ship.center_ship()

            time.sleep(0.5)
        else:
            self.stats.game_active = False

    # Определение поведения пуль

    def _fire_bullet(self):
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_bullets(self):
        # Удаление вышедших за границы экрана снарядов
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_invaders_collision()

    def _check_bullet_invaders_collision(self):
        # Удаление снаряда и пришельца (коллизия между элементами)
        # Тут можно третьим аргументом передать False, чтобы снаряд не убивался об первого пришельца
        # collisions = pygame.sprite.groupcollide(self.bullets, self.invaders, True, True)

        # Тестовый залп
        collisions = pygame.sprite.groupcollide(self.bullets, self.invaders, False, True)
        if collisions:
            self.stats.score += self.settings.invader_point
            self.score_table.prep_score()

        # Обновление флота при уничтожении всех пришельцев
        if not self.invaders:
            self.bullets.empty()
            self._create_armada()
            self.settings.increase_speed()  # Увеличение настроек игры

            self.stats.level += 1
            self.score_table.prep_level()

    def _check_invaders_bottom_collision(self):
        screen_rect = self.screen.get_rect()
        for invader in self.invaders.sprites():
            if invader.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _update_screen(self):
        self.screen.blit(self.background_image, (0, 0))
        self.ship.blitMe()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.invaders.draw(self.screen)

        if not self.stats.game_active:
            self.play_button.draw_button()

        # Отображение различных статистик на экране
        self.score_table.show_life()
        self.score_table.show_score()
        pygame.display.flip()

    # Проверки для клавиш

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                self._check_play_button(mouse_position)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()  # Сброс игровых настроек
            self.stats.reset_stats()  # Сброс игровой статистики
            self.stats.game_active = True

            self.score_table.prep_score()
            self.score_table.prep_level()
            self.score_table.prep_life()

            self.invaders.empty()
            self.bullets.empty()
            self._create_armada()
            self.ship.center_ship()


if __name__ == "__main__":
    ai = SpaceInvaders()
    ai.run_game()
