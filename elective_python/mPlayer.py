import pygame

player_controls = {
    "1": [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d],
    "2": [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
}

class Player:
    def __init__(self, hitbox: tuple, player_no: str):
        self.Hitbox = pygame.Rect(hitbox)
        self.Speed = 150
        self.Controls = player_controls[player_no]

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[self.Controls[0]]:
            self.Hitbox.y -= self.Speed * dt
        if keys[self.Controls[1]]:
            self.Hitbox.y += self.Speed * dt
        if keys[self.Controls[2]]:
            self.Hitbox.x -= self.Speed * dt
        if keys[self.Controls[3]]:
            self.Hitbox.x += self.Speed * dt

    def render(self, surface: pygame.Surface):
        pygame.draw.rect(surface, (255, 255, 255), self.Hitbox)