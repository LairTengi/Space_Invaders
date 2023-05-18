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
        self.life_rect.right = self.screen_rect.right - 500
        self.life_rect.top = 10

    def prep_level(self):
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                                            self.text_color, self.settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 600
        self.level_rect.top = 10

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)

    def show_life(self):
        self.screen.blit(self.life_image, self.life_rect)
