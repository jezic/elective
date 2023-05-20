import pygame

class Button:
    def __init__(self, width, height) -> None:
        self.X = 0
        self.Y = 0
        self.Width = width
        self.Height = height
        self.Color = (255, 255, 255)
        self.Pressed = False
        self.Activated = False

    def setPosition(self, x, y):
        self.X = x
        self.Y = y

    def handleEvents(self, event: pygame.event):
        pos = pygame.Vector2(0, 0)
                
        if (event.type == pygame.MOUSEBUTTONDOWN):
            pos = pygame.Vector2(pygame.mouse.get_pos())

            if ((pos.x > self.X) and (pos.x < self.X + self.Width) and (pos.y > self.Y) and (pos.y < self.Y + self.Height)):
                self.Color = (128, 128, 128)
                self.Pressed = True

        if (self.Pressed):
            if (event.type == pygame.MOUSEBUTTONUP):
                pos = pygame.Vector2(pygame.mouse.get_pos())
                self.Pressed = False
                if ((pos.x > self.X) and (pos.x < self.X + self.Width) and (pos.y > self.Y) and (pos.y < self.Y + self.Height)):
                    self.Activated = True
                    self.color = (255, 0, 0)

    def render(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.Color, (self.X, self.Y, self.Width, self.Height))
