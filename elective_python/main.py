import mStates
import pygame

def main():
    pygame.init()

    pygame.display.set_caption("Group 1 Elective Python: Cold Wheels")
    
    screen = pygame.display.set_mode((640, 360))
    clock = pygame.time.Clock()
    running = True
    dt = clock.tick(60) / 1000
    
    gCurrentState = mStates.MainMenu(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            gCurrentState.handleEvents(event)
            
        screen.fill("black")

        gCurrentState.update(dt)

        if gCurrentState.ChangeState:
            if gCurrentState.NextState == None:
                running = False
            else:
                gCurrentState = gCurrentState.NextState

        gCurrentState.render(screen)
        pygame.display.flip()

        dt = clock.tick(60) / 1000  # limits FPS to 60

    pygame.mixer.init()
    pygame.font.quit()
    pygame.quit()

main()