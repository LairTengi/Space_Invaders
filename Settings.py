import math


class Settings:
    def __init__(self):
        self.screen_width = 640
        self.screen_height = 600
        self.bg_color = (0, 0, 0)  # Фон для текста

        self.ship_limit = 2  # По факту тут три жизни корабля
        self.speedup_scale = 1.1

        self.score = 0
        self.invader_point = 50  # Стоимость пришельца

        # Параметры обычных пуль
        self.bullet_width = 3
        # self.bullet_width = 640           Заряд для тестирования
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)

        # Параметры супер бомбы
        self.bomb_width = 250
        self.bomb_height = 15
        self.bomb_color = (0, 255, 0)
        self.bomb_limit = 3        # Три супер бомбы на игру

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.speed_ship = 2
        self.bullet_speed = 2.0
        self.bomb_speed = 2.0
        self.invader_speed = 1

        self.armada_direction = 1
        self.armada_drop_speed = 5

    # Функция увеличения скорости игры
    def speedup_bullet_invader(self, current_speed):
        max_speed_increase_invaders = 1.3
        new_speed = current_speed + math.log(current_speed + 0.00005, 2)
        if current_speed >= max_speed_increase_invaders:
            return current_speed
        return min(new_speed, max_speed_increase_invaders)

    def speedup_armada(self, current_speed):
        max_speed_armada = 30
        slowdown = 0.75
        new_speed = current_speed * slowdown + math.log(current_speed, 2)
        if current_speed >= max_speed_armada:
            return current_speed
        return min(new_speed, max_speed_armada)

    def increase_speed(self):
        self.bullet_speed = self.speedup_bullet_invader(self.bullet_speed)
        self.invader_speed = self.speedup_bullet_invader(self.invader_speed)
        self.bomb_speed = self.speedup_bullet_invader(self.bomb_speed)
        self.armada_drop_speed = self.speedup_armada(self.armada_drop_speed)
