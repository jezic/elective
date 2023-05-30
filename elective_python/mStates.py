import mButton
import pygame
import mPlayer

pygame.font.init()

def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

class States:
    def handleEvents(self, event: pygame.event):
        pass
    def update(self, dt):
        pass
    def render(self, surface: pygame.Surface):
        pass

class MainMenu(States):
    BG_TEXTURE = pygame.transform.scale(pygame.image.load("elective_python/imgs/bg1.png"), (640, 360))
    CRISTIK_FONT = pygame.font.SysFont("cristik", 38)
    def __init__(self, screen: pygame.Surface):
        self.Screen = screen
        self.Width = screen.get_width()
        self.Height = screen.get_height()

        self.StartButton = mButton.Button(128, 48)
        self.StartButton.setPosition((self.Width - self.StartButton.Width) / 2, 205)
        self.QuitButton = mButton.Button(128, 48)
        self.QuitButton.setPosition((self.Width - self.StartButton.Width) / 2, 285)

        self.StartText = self.CRISTIK_FONT.render("START", True, (0, 74, 173))
        self.QuitText = self.CRISTIK_FONT.render("QUIT", True, (255, 32, 32))
        self.ArrowText = self.CRISTIK_FONT.render(">", True, (0, 0, 0))

        self.ChangeState = False
        self.NextState = None
        print("MAIN MENU STATE")

    def handleEvents(self, event: pygame.event):
        self.StartButton.handleEvents(event)
        self.QuitButton.handleEvents(event)
            
    
    def update(self, dt):
        if (self.StartButton.Activated):
            self.ChangeState = True
            self.NextState = CustomizeState(self.Screen)
        elif self.QuitButton.Activated:
            self.ChangeState = True


    def render(self, surface: pygame.Surface):
        surface.blit(self.BG_TEXTURE, (0,0))
        
        surface.blit(self.StartText, 
                     ((self.Width - self.StartText.get_width()) / 2, 
                      (205 + (self.StartButton.Height - self.StartText.get_height()) / 2)))
        surface.blit(self.QuitText, 
                     ((self.Width - self.QuitText.get_width()) / 2, 
                      (285 + (self.QuitButton.Height - self.QuitText.get_height()) / 2)))
        if self.StartButton.Hovered:
            surface.blit(self.ArrowText,
                        ((self.Width - 170) / 2, 
                        205))
        elif self.QuitButton.Hovered:
            surface.blit(self.ArrowText,
                        ((self.Width - 170) / 2, 
                        290))


class CustomizeState(States):
    BG_TEXTURE = pygame.transform.scale(pygame.image.load("elective_python/imgs/bg2.png"), (640, 360))
    CRISTIK_FONT = pygame.font.SysFont("cristik", 36)
    CRISTIK_FONT_L = pygame.font.SysFont("cristik", 50)

    CAR_SIDE_TEXTURES = [scale_image(pygame.image.load("elective_python/imgs/Car1 side.png"), 0.3), 
                         scale_image(pygame.image.load("elective_python/imgs/Car2side.png"), 0.5)]

    def __init__(self, screen: pygame.Surface):
        self.Screen = screen
        self.Width = screen.get_width()
        self.Height = screen.get_height()

        self.ChangeState = False
        self.NextState = None
        print("CUSTOMIZE MENU STATE")

        self.DisplayCarNo = 0
        self.PlayerNoDisplay = 0
        self.Car1_Texture = 0
        self.Car2_Texture = 0

        self.PlayButton = mButton.Button(128, 48)
        self.PlayButton.setPosition((self.Width - self.PlayButton.Width), 
                                    (self.Height - self.PlayButton.Height))
        self.BackButton = mButton.Button(128, 48)
        self.BackButton.setPosition((0),
                                    (self.Height - self.BackButton.Height))
        
        self.RightArrowButton = mButton.Button(30, 40)
        self.RightArrowButton.setPosition((self.Width - self.RightArrowButton.Width), 
                                    (self.Height - self.RightArrowButton.Height) / 2)
        self.RightArrowText = self.CRISTIK_FONT_L.render(">", True, (0, 74, 173))
        
        self.LeftArrowButton = mButton.Button(30, 40)
        self.LeftArrowButton.setPosition(0, 
                                    (self.Height - self.RightArrowButton.Height) / 2)
        self.LeftArrowText = self.CRISTIK_FONT_L.render("<", True, (0, 74, 173))
        
        self.PlayText = self.CRISTIK_FONT.render("PLAY", True, (0, 74, 173))
        self.BackText = self.CRISTIK_FONT.render("BACK", True, (255, 32, 32))

        self.SelectText = self.CRISTIK_FONT.render("SELECT", True, ((0, 74, 173)))
        self.PlayerNoTexts = [self.CRISTIK_FONT_L.render("Player One", True, (0, 74, 173)),
                              self.CRISTIK_FONT_L.render("Player Two", True, (255, 32, 32))]
    
    def handleEvents(self, event: pygame.event):
        self.PlayButton.handleEvents(event)
        self.BackButton.handleEvents(event)
        self.RightArrowButton.handleEvents(event)
        self.LeftArrowButton.handleEvents(event)

    def update(self, dt):
        if self.RightArrowButton.Activated:
            self.DisplayCarNo = 1
        elif self.LeftArrowButton.Activated:
            self.DisplayCarNo = 0

        match self.PlayerNoDisplay:
            case 0:
                if self.BackButton.Activated:
                    self.ChangeState = True
                    self.NextState = MainMenu(self.Screen)
                elif self.PlayButton.Activated:
                    self.PlayerNoDisplay = 1
                    self.PlayButton.Activated = False
                    self.Car1_Texture = self.DisplayCarNo
                    self.DisplayCarNo = 0
            case 1:
                if self.BackButton.Activated:
                    self.DisplayCarNo = 0
                    self.PlayerNoDisplay = 0
                    self.BackButton.Activated = False
                elif self.PlayButton.Activated:
                    self.Car2_Texture = self.DisplayCarNo
                    self.ChangeState = True
                    self.NextState = PlayState(self.Screen, self.Car1_Texture, self.Car2_Texture)

    def render(self, surface: pygame.Surface):
        surface.blit(self.BG_TEXTURE, (0,0))

        surface.blit(self.CAR_SIDE_TEXTURES[self.DisplayCarNo], ((self.Width - self.CAR_SIDE_TEXTURES[self.DisplayCarNo].get_width()) / 2
            , (self.Height - self.CAR_SIDE_TEXTURES[self.DisplayCarNo].get_height()) / 2))
        
        if self.PlayerNoDisplay == 0:
            surface.blit(self.SelectText, 
                        ((self.Width - self.PlayButton.Width) + 
                        (self.PlayButton.Width - self.SelectText.get_width()) / 2, 
                        (self.Height - self.SelectText.get_height()) - 
                        (self.PlayButton.Height - self.SelectText.get_height()) / 2))
        else:
            surface.blit(self.PlayText, 
                        ((self.Width - self.PlayButton.Width) + 
                        (self.PlayButton.Width - self.PlayText.get_width()) / 2, 
                        (self.Height - self.PlayText.get_height()) - 
                        (self.PlayButton.Height - self.PlayText.get_height()) / 2))
                
        surface.blit(self.LeftArrowText, ((self.LeftArrowButton.Width - self.LeftArrowText.get_width()) / 2, 
                                        ((self.Height - self.LeftArrowButton.Height)/2) +
                                        (self.RightArrowButton.Height - self.RightArrowText.get_height()) / 2))

        surface.blit(self.RightArrowText, ((self.Width - self.RightArrowButton.Width) +
                                        (self.RightArrowButton.Width - self.RightArrowText.get_width()) / 2,
                                        ((self.Height - self.RightArrowButton.Height) / 2) +
                                        (self.RightArrowButton.Height - self.RightArrowText.get_height()) / 2))
        
        surface.blit(self.PlayerNoTexts[self.PlayerNoDisplay], 
                    ((self.Width - self.PlayerNoTexts[self.PlayerNoDisplay].get_width()) / 2, 0))        
             
        surface.blit(self.BackText, 
                     ((self.BackButton.Width - self.BackText.get_width()) / 2, 
                      (self.Height - self.BackText.get_height()) - 
                      (self.BackButton.Height - self.BackText.get_height()) / 2))


class PlayState(States):
    CAR_TEXTURES = [scale_image(pygame.image.load("elective_python/imgs/Car 1.png"), 0.03),
                    scale_image(pygame.image.load("elective_python/imgs/Car 2.png"), 0.03)]
    TRACK = pygame.transform.scale(pygame.image.load("elective_python/imgs/Snowy map.png"), (640, 360))

    def __init__(self, screen: pygame.Surface, car1_texture, car2_texture):
        screen = pygame.display.set_mode((640, 480))
        self.Width = screen.get_width()
        self.Height = screen.get_height()
        self.ChangeState = False
        self.NextState = States()
        self.Player1 = mPlayer.Player(self.CAR_TEXTURES[car1_texture], "1")
        self.Player2 = mPlayer.Player(self.CAR_TEXTURES[car2_texture], "2")
        print("PLAY STATE")

    def handleEvents(self, event: pygame.event):
        pass
    
    def update(self, dt):
        self.Player1.update(dt)
        self.Player2.update(dt)

    def render(self, surface: pygame.Surface):
        surface.blit(self.TRACK, (0, 0))
        self.Player1.render(surface)
        self.Player2.render(surface)
        