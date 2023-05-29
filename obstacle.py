import pygame


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, velocity=5.0, height=695):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("images/water_greenish.png"), (49, 70)
        )
        self.rect = self.image.get_rect()
        self.size_x = self.image.get_width()
        self.size_y = self.image.get_height()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.velocity = velocity
        self.height = height

    def update(self):
        self.rect.y += self.velocity

    def draw(self, screen):
        screen.blit(self.image, self.rect)
