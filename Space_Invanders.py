import pickle
import sys
import time

import pygame

from Bullets.Bullet import Bullet
from Bullets.Bomb import Bomb
from Settings import Settings
from Ship import Ship
from Invader import Invader
from Stats.GameStatistics import GameStats
from Stats.ScoreTable import ScoreTable
from Buttons.Button import Button


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
        self.bomb = pygame.sprite.Group()
        self._create_armada()

        # Игровая статистика
        self.stats = GameStats(self)
        self.score_table = ScoreTable(self)

        # Кнопка Play
        self.play_button = Button(self, "Play")

        self.FIRST_GAME = True

    def run_game(self):
        self.load_stats()  # Загрузка сериализованных объектов
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_invaders()
                self._update_bomb()

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

    def _fire_bomb(self):
        # Проверка на 3 заряда
        if self.stats.bombs_left > 0:
            self.stats.bombs_left -= 1
            self.score_table.prep_bombs()
        elif self.stats.bombs_left == 0:
            return

        new_bomb = Bomb(self)
        self.bomb.add(new_bomb)

    def _update_bullets(self):  # Удаление вышедших за границы экрана пуль
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_invaders_collision()

    def _update_bomb(self):  # Удаление бомб за границами экрана
        self.bomb.update()
        for bomb in self.bomb.copy():
            if bomb.rect.bottom <= 0:
                self.bomb.remove(bomb)
        self._check_bullet_invaders_collision()

    def _check_bullet_invaders_collision(self):
        # Удаление снаряда и пришельца (коллизия между элементами)
        # Тут можно третьим аргументом передать False, чтобы снаряд не убивался об первого пришельца
        collisions = pygame.sprite.groupcollide(self.bullets, self.invaders, True, True)

        collisions_bomb = pygame.sprite.groupcollide(self.bomb, self.invaders, False, True)

        # Тестовый залп
        # collisions = pygame.sprite.groupcollide(self.bullets, self.invaders, False, True)
        if collisions or collisions_bomb:
            self.stats.score += self.settings.invader_point
            self.score_table.prep_score()
            self.score_table.check_new_record()

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
        for bomb in self.bomb.sprites():
            bomb.draw_bomb()
        self.invaders.draw(self.screen)

        if not self.stats.game_active:
            self.play_button.draw_button()

        # Отображение статистик на экране
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
            self.graceful_shutdown()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_b:  # Кнопка b для бомбы
            self._fire_bomb()
        elif event.key == pygame.K_p and not self.stats.game_active:
            if self.FIRST_GAME:
                self._prepare_game()
                self.FIRST_GAME = False
            else:
                self.stats.game_active = True
        elif event.key == pygame.K_p and self.stats.game_active:
            self.stats.game_active = False

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._prepare_game()

    def _prepare_game(self):
        if not self.stats.game_active:
            self.settings.initialize_dynamic_settings()  # Сброс игровых настроек
            self.stats.reset_stats()  # Сброс игровой статистики
            self.stats.game_active = True

            self.score_table.prep_score()
            self.score_table.prep_level()
            self.score_table.prep_life()
            self.score_table.prep_bombs()
            self.score_table.prep_high_score()

            self.invaders.empty()
            self.bullets.empty()
            self._create_armada()
            self.ship.center_ship()

    # Красивый выход
    def graceful_shutdown(self):
        self.save_stats()
        sys.exit(0)

    def save_stats(self):
        serialized_data = pickle.dumps(self.stats.high_score)
        with open('data.pickle', 'wb') as file:
            file.write(serialized_data)

    def load_stats(self):
        try:
            with open('data.pickle', 'rb') as file:
                loaded_data = pickle.load(file)
            self.stats.high_score = int(loaded_data)
        except:
            pass


if __name__ == "__main__":
    ai = SpaceInvaders()
    ai.run_game()
