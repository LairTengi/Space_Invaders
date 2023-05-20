class GameStats():
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
        self.high_score = 0  # Счёт рекорда

    def reset_stats(self):
        # Отдельная инициализация статистики, которая изменяется в ходе игры
        self.ships_left = self.settings.ship_limit
        self.score = self.settings.score  # Очки
        self.level = 1  # Уровень игры
