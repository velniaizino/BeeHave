import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image, scale):
        super().__init__()
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
        self.size_x = self.image.get_width()
        self.size_y = self.image.get_height()
        self.clicked = False

    def draw(self, screen):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action
