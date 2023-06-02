import mButton
import pygame
import mPlayer

pygame.font.init()
pygame.mixer.init()

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
    BG_TEXTURE = pygame.transform.scale(pygame.image.load("assets/imgs/bg1.png"), (640, 360))
    CRISTIK_FONT = pygame.font.Font("assets/fonts/Cristik.ttf", 38)
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

        pygame.mixer.music.stop()
        self.Lobby_Sound = pygame.mixer.music.load("assets/fx/lobby_sound.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

    def handleEvents(self, event: pygame.event):
        self.StartButton.handleEvents(event)
        self.QuitButton.handleEvents(event)
            
    
    def update(self, dt):
        if self.StartButton.Activated:
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
    BG_TEXTURE = pygame.transform.scale(pygame.image.load("assets/imgs/bg2.png"), (640, 360))
    CRISTIK_FONT = pygame.font.Font("assets/fonts/Cristik.ttf", 36)
    CRISTIK_FONT_L = pygame.font.Font("assets/fonts/Cristik.ttf", 50)

    CAR_SIDE_TEXTURES = [scale_image(pygame.image.load("assets/imgs/Car1 side.png"), 0.3), 
                         scale_image(pygame.image.load("assets/imgs/Car2side.png"), 0.5)]
    
    CAR_SOUNDS = [pygame.mixer.Sound("assets/fx/car_1_sound.mp3"),
                  pygame.mixer.Sound("assets/fx/car_2_sound.mp3")]

    def __init__(self, screen: pygame.Surface):
        self.Screen = screen
        self.Width = screen.get_width()
        self.Height = screen.get_height()

        self.ChangeState = False
        self.NextState = None

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
        pygame.mixer.Sound.play(self.CAR_SOUNDS[0])
        
        
    
    def handleEvents(self, event: pygame.event):
        self.PlayButton.handleEvents(event)
        self.BackButton.handleEvents(event)
        self.RightArrowButton.handleEvents(event)
        self.LeftArrowButton.handleEvents(event)

    def update(self, dt):
        if self.RightArrowButton.Activated:
            self.DisplayCarNo = 1
            pygame.mixer.Sound.play(self.CAR_SOUNDS[1])
        elif self.LeftArrowButton.Activated:
            self.DisplayCarNo = 0
            pygame.mixer.Sound.play(self.CAR_SOUNDS[0])

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

        surface.blit(self.CAR_SIDE_TEXTURES[self.DisplayCarNo], 
                     ((self.Width - self.CAR_SIDE_TEXTURES[self.DisplayCarNo].get_width()) / 2
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
    CAR_TEXTURES = [scale_image(pygame.image.load("assets/imgs/Car 1.png"), 0.015),
                    scale_image(pygame.image.load("assets/imgs/Car 2.png"), 0.015)]
    TRACK = pygame.transform.scale(pygame.image.load("assets/imgs/track.png"), (640, 360))
    TRACK_BORDER = pygame.transform.scale(pygame.image.load("assets/imgs/track_border.png"), (640, 360))
    TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

    CRISTIK_FONT = pygame.font.Font("assets/fonts/Cristik.ttf", 36)
    CRISTIK_FONT_L = pygame.font.Font("assets/fonts/Cristik.ttf", 50)

    def __init__(self, screen: pygame.Surface, car1_texture, car2_texture):
        self.Width = screen.get_width()
        self.Height = screen.get_height()
        self.Screen = screen
        self.ChangeState = False
        self.NextState = States()
        self.Win = 0

        self.CAR_TEXTURES[0].set_alpha(255)
        self.CAR_TEXTURES[1].set_alpha(255)
        self.TRACK.set_alpha(255)

        self.Player1 = mPlayer.Player(self.CAR_TEXTURES[car1_texture], "1")
        self.Player1.setPosition(33, 175)

        self.Player2 = mPlayer.Player(self.CAR_TEXTURES[car2_texture], "2")
        self.Player2.setPosition(55, 175)

        self.Player1.initializePowerUp(car1_texture, self.Player2)
        self.Player2.initializePowerUp(car2_texture, self.Player1)

        self.FinishLine2 = pygame.Rect(35, 220, 50, 5)
        self.WinnerText = self.CRISTIK_FONT.render("", True, (0, 74, 173))

        self.QuitButton = mButton.Button(128, 48)
        self.QuitButton.setPosition((self.Width - self.QuitButton.Width) / 2, 
                                     (self.Height - self.QuitButton.Height) / 2 + 50)
        self.QuitText = self.CRISTIK_FONT.render("QUIT", True, (255, 32, 32))

        pygame.mixer.music.stop()
        pygame.mixer.music.load("assets/fx/race_sound.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
        

    def handleEvents(self, event: pygame.event):
        self.QuitButton.handleEvents(event)
        self.Player1.handleEvents(event)
        self.Player2.handleEvents(event)
    
    def update(self, dt):
        if self.Win == 0:
            self.Player1.update(dt, self.TRACK_BORDER_MASK, 0, 0)
            self.Player2.update(dt, self.TRACK_BORDER_MASK, 0, 0)

            if ((self.Player1.X > self.FinishLine2.x) and 
                (self.Player1.X < self.FinishLine2.x + self.FinishLine2.width) and
                (self.Player1.Y > self.FinishLine2.y) and 
                (self.Player1.Y < self.FinishLine2.y + self.FinishLine2.height)):
                self.Win = 1

            if ((self.Player2.X > self.FinishLine2.x) and 
                (self.Player2.X < self.FinishLine2.x + self.FinishLine2.width) and
                (self.Player2.Y > self.FinishLine2.y) and 
                (self.Player2.Y < self.FinishLine2.y + self.FinishLine2.height)):
                self.Win = 2
        elif self.Win == 1:
            self.WinnerText = self.CRISTIK_FONT.render("Player 1 Wins!", True, ((0, 74, 173)))
            if self.QuitButton.Activated:
                self.ChangeState = True
                self.NextState = MainMenu(self.Screen)
        elif self.Win == 2:
            self.WinnerText = self.CRISTIK_FONT.render("Player 2 Wins!", True, ((0, 74, 173)))
            if self.QuitButton.Activated:
                self.ChangeState = True
                self.NextState = MainMenu(self.Screen)


    def render(self, surface: pygame.Surface):
        surface.blit(self.TRACK, (0, 0))
        if self.Win != 0:
            surface.blit(self.WinnerText, 
                         ((self.Width - self.WinnerText.get_width()) / 2, 
                          (self.Height - self.WinnerText.get_height()) / 2))
            self.TRACK.set_alpha(20)
            self.CAR_TEXTURES[0].set_alpha(20)
            self.CAR_TEXTURES[1].set_alpha(20)
            surface.blit(self.QuitText, 
                     ((self.Width - self.QuitText.get_width()) / 2, 
                      (50 + (self.Height - self.QuitText.get_height()) / 2)))
            
        self.Player1.render(surface)
        self.Player2.render(surface)
        