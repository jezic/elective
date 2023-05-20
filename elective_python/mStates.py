import mButton
import pygame
import mPlayer

class States:
    def handleEvents(self, event: pygame.event):
        pass

    def update(self, dt):
        pass

    def render(self, surface: pygame.Surface):
        pass

class MainMenu(States):
    def __init__(self, width, height):
        self.Width = width
        self.Height = height
        self.StartButton = mButton.Button(100, 50)
        self.StartButton.setPosition((self.Width - self.StartButton.Width) / 2, (self.Height- self.StartButton.Height) / 2)
        self.ChangeState = False
        self.NextState = States()
        print("MAIN MENU STATE")

    def handleEvents(self, event: pygame.event):
        self.StartButton.handleEvents(event)
    
    def update(self, dt):
        if (self.StartButton.Activated):
            self.ChangeState = True
            self.NextState = PlayState(self.Width, self.Height)

    def render(self, surface: pygame.Surface):
        self.StartButton.render(surface)
        pass

class PlayState(States):
    def __init__(self, width, height):
        self.Width = width
        self.Height = height
        self.ChangeState = False
        self.NextState = States()
        self.Player1 = mPlayer.Player((0, 0, 10, 10), "1")
        self.Player2 = mPlayer.Player((0, 0, 10, 10), "2")
        print("CUSTOMIZE STATE")

    def handleEvents(self, event: pygame.event):
        pass
    
    def update(self, dt):
        self.Player1.update(dt)
        self.Player2.update(dt)

    def render(self, surface: pygame.Surface):
        self.Player1.render(surface)
        self.Player2.render(surface)