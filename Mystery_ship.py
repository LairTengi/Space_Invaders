import pygame

from pygame.sprite import Sprite


class MysteryShip(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.image.load('images/mistery_ship.png')
        self.rect = self.image.get_rect()
        # Местоположение мистического корабля
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    # Движение то же, что и у обычных пришельцев
    def update(self):
        self.x += (self.settings.invader_speed * self.settings.armada_direction)
        self.rect.x = self.x

    # Проверка границ
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    # Отрисовка
    def draw(self, surface):
        surface.blit(self.image, self.rect)
