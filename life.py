import pygame


class Life(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("images/heart.png"), (30, 30)
        )
        self.rect = self.image.get_rect()
        self.size_x = self.image.get_width()
        self.size_y = self.image.get_height()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def loose_life(self):
        self.image = pygame.transform.scale(
            pygame.image.load("images/grey_heart.png"), (30, 30)
        )

    def get_life(self):
        self.image = pygame.transform.scale(
            pygame.image.load("images/heart.png"), (30, 30)
        )

    def draw(self, screen):
        screen.blit(self.image, self.rect)
