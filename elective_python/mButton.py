import pygame

class Button:
    def __init__(self, width, height) -> None:
        self.X = 0
        self.Y = 0
        self.Width = width
        self.Height = height
        self.Pressed = False
        self.Activated = False
        self.Hovered = False

    def setPosition(self, x, y):
        self.X = x
        self.Y = y

    def handleEvents(self, event: pygame.event):
        pos = pygame.Vector2(0, 0)
        self.Activated = False
        if (event.type == pygame.MOUSEMOTION):
            pos = pygame.Vector2(pygame.mouse.get_pos())

            if ((pos.x > self.X) and (pos.x < self.X + self.Width) and (pos.y > self.Y) and (pos.y < self.Y + self.Height)):
                self.Hovered = True
            else:
                self.Hovered = False

        if (event.type == pygame.MOUSEBUTTONDOWN):
            pos = pygame.Vector2(pygame.mouse.get_pos())

            if ((pos.x > self.X) and (pos.x < self.X + self.Width) and (pos.y > self.Y) and (pos.y < self.Y + self.Height)):
                self.Pressed = True

        if (self.Pressed):
            if (event.type == pygame.MOUSEBUTTONUP):
                pos = pygame.Vector2(pygame.mouse.get_pos())
                self.Pressed = False
                if ((pos.x > self.X) and (pos.x < self.X + self.Width) and (pos.y > self.Y) and (pos.y < self.Y + self.Height)):
                    self.Activated = True

    #for debugging purposes only
    def render(self, surface: pygame.Surface, color):
        pygame.draw.rect(surface, color, (self.X, self.Y, self.Width, self.Height))
