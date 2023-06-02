import pygame
import math

def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

player_controls = {
    "1": [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d],
    "2": [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
}

class SpeedSkill:
    SKILL_TEXTURE = scale_image(pygame.image.load("assets/imgs/Boostlogo.png"), 0.015)
    def __init__(self, player):
        self.StartTime = 0
        self.Started = False
        self.Boost = 200
        self.Player = player
        self.OriginalMaxVel = player.Max_Vel

    def handleEvents(self, event: pygame.event, key):
        if self.Started == False:
            if event.type == pygame.KEYDOWN:
                if event.key == key:
                    self.StartTime = pygame.time.get_ticks()
                    self.Player.Max_Vel += self.Boost
                    self.Started = True
    
    def update(self, dt):
        if self.Started:
            time_elapsed = pygame.time.get_ticks() - self.StartTime
            if time_elapsed >= 5000:
                self.Player.Max_Vel = self.OriginalMaxVel
                self.Started = False

    def render(self, surface):
        if self.Started:
            surface.blit(self.SKILL_TEXTURE,
                     ((self.Player.X + 10),
                      (self.Player.Y)))

class SlowSkill:
    SKILL_TEXTURE = scale_image(pygame.image.load("assets/imgs/Slowlogo.png"), 0.015)
    def __init__(self, player):
        self.StartTime = 0
        self.Started = False
        self.SlowDown = 50
        self.Player = player
        self.OriginalMaxVel = player.Max_Vel
    
    def handleEvents(self, event: pygame.event, key):
        if self.Started == False:
            if event.type == pygame.KEYDOWN:
                if event.key == key:
                    self.Player.Max_Vel -= 100
                    self.StartTime = pygame.time.get_ticks()
                    self.Started = True
    
    def update(self, dt):
        if self.Started:
            time_elapsed = pygame.time.get_ticks() - self.StartTime
            
            if time_elapsed >= 3000:
                self.Player.Max_Vel = self.OriginalMaxVel
                self.Started = False

    def render(self, surface):
        if self.Started:
            surface.blit(self.SKILL_TEXTURE,
                     ((self.Player.X + 10,
                      (self.Player.Y))))

class Player:
    def __init__(self, texture: pygame.Surface, player_no: str):
        self.Texture = texture
        self.Max_Vel = 150
        self.Vel = 0.0
        self.Rotation_Vel = 4.0
        self.Angle = 0.0
        self.X = 0.0 
        self.Y = 0.0
        self.Acceleration = 1.5
        self.Controls = player_controls[player_no]
        self.Collided = False
        self.POI = None
        self.PowerUp = None

    def initializePowerUp(self, texture_no: int, enemy_player):
        if texture_no == 0:
            self.PowerUp = SlowSkill(enemy_player)
        elif texture_no == 1:
            self.PowerUp = SpeedSkill(self)

    def setPosition(self, x, y):
        self.X = x
        self.Y = y

    def rotate(self, left=False, right = True):
        if left:
            self.Angle += self.Rotation_Vel
        elif right:
            self.Angle -= self.Rotation_Vel
    
    def handleEvents(self, event: pygame.event):
        self.PowerUp.handleEvents(event, self.Controls[1])

    def update(self, dt, mask: pygame.Mask, x, y):
        keys = pygame.key.get_pressed()
        moved = False

        if not self.Collided:
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
            self.Vel = max(self.Vel - self.Acceleration / 3, 0)
            radians = math.radians(self.Angle)
            vertical = math.cos(radians) * self.Vel
            horizontal = math.sin(radians) * self.Vel

            self.Y -= vertical * dt
            self.X -= horizontal * dt

        car_mask = pygame.mask.from_surface(self.Texture)
        offset = (self.X - x, self.Y - y)
        self.POI= mask.overlap(car_mask,offset)
        self.Collided = False
        if self.POI != None:
            self.Collided = True
            moved = True
            self.Vel = -45
            radians = math.radians(self.Angle)
            vertical = math.cos(radians) * self.Vel
            horizontal = math.sin(radians) * self.Vel

            self.Y -= vertical * dt
            self.X -= horizontal * dt

        self.PowerUp.update(dt)

    def getNewCarImageRect(self):
        rotated_image = pygame.transform.rotate(self.Texture, self.Angle)
        new_rect = rotated_image.get_rect(center=self.Texture.get_rect(topleft=(self.X, self.Y)).center)

        return (rotated_image, new_rect)

    def render(self, surface: pygame.Surface):
        new_rect = self.getNewCarImageRect()
        surface.blit(new_rect[0], new_rect[1].topleft)
        self.PowerUp.render(surface)