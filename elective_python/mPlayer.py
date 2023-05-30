import pygame
import math

player_controls = {
    "1": [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d],
    "2": [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
}



class Player:
    def __init__(self, texture: pygame.Surface, player_no: str):
        self.Texture = texture
        self.Max_Vel = 150
        self.Vel = 0.0
        self.Rotation_Vel = 4.0
        self.Angle = 0.0
        self.X, self.Y = (0, 0)
        self.Acceleration = 2.0
        self.Controls = player_controls[player_no]

    def rotate(self, left=False, right = True):
        if left:
            self.Angle += self.Rotation_Vel
        elif right:
            self.Angle -= self.Rotation_Vel

    def update(self, dt):
        keys = pygame.key.get_pressed()
        moved = False

        if keys[self.Controls[2]]:
            self.rotate(left = True)
        if keys[self.Controls[3]]:
            self.rotate(right=True)
        if keys[self.Controls[0]]:
            moved = True
            self.Vel = min(self.Vel + self.Acceleration, self.Max_Vel)
            radians = math.radians(self.Angle)
            vertical = math.cos(radians) * self.Vel
            horizontal = math.sin(radians) * self.Vel

            self.Y -= vertical * dt
            self.X -= horizontal * dt
        
        if not moved:
            self.Vel = max(self.Vel - self.Acceleration, 0)
            radians = math.radians(self.Angle)
            vertical = math.cos(radians) * self.Vel
            horizontal = math.sin(radians) * self.Vel

            self.Y -= vertical * dt
            self.X -= horizontal * dt

    def render(self, surface: pygame.Surface):
        rotated_image = pygame.transform.rotate(self.Texture, self.Angle)
        new_rect = rotated_image.get_rect(center=self.Texture.get_rect(topleft=(self.X, self.Y)).center)
        surface.blit(rotated_image, new_rect.topleft)