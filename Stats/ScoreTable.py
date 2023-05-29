import pygame.font


class ScoreTable():
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('arial', 24)
        self.prep_score()
        self.prep_life()
        self.prep_level()
        self.prep_high_score()
        self.prep_bombs()

    def prep_score(self):
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 10
        self.score_rect.top = 10

    def prep_life(self):
        life_str = str(self.stats.ships_left + 1)
        self.life_image = self.font.render(life_str, True,
                                           self.text_color, self.settings.bg_color)
        self.life_rect = self.life_image.get_rect()
        self.life_rect.right = self.screen_rect.right - 550
        self.life_rect.top = 10

    def prep_level(self):
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                                            self.text_color, self.settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 600
        self.level_rect.top = 10

    def prep_high_score(self):
        high_score = self.stats.high_score  # Не округляем
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color, self.settings.bg_color)
        # Выравнивание по центру
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_bombs(self):
        bombs = str(self.stats.bombs_left)
        self.bombs_image = self.font.render(bombs, True,
                                            self.text_color, self.settings.bg_color)
        self.bombs_rect = self.bombs_image.get_rect()
        self.bombs_rect.right = self.screen_rect.right - 500
        self.bombs_rect.top = 10

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.bombs_image, self.bombs_rect)

    def show_life(self):
        self.screen.blit(self.life_image, self.life_rect)

    def check_new_record(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
