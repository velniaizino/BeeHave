import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.sprites.append(
            pygame.transform.scale(pygame.image.load("images/Bee1.png"), (98, 88))
        )
        self.sprites.append(
            pygame.transform.scale(pygame.image.load("images/Bee2.png"), (98, 88))
        )
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.size_x = self.image.get_width()
        self.size_y = self.image.get_height()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.lives = 3

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.current_sprite += 0.2
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
