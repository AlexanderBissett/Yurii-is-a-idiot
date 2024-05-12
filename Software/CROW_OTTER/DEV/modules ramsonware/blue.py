import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()
blue = 53, 126, 199
text_wr = 255, 255, 255
background = 53, 126, 199

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
size = SCREEN_WIDTH, SCREEN_HEIGHT

#font = pygame.font.Font('freesansbold.ttf', 32)
font = pygame.font.SysFont(None, 48)
#img = font.render(font, True, red)
text = font.render(':(', True, text_wr, blue)
textRect = text.get_rect()
textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


screen = pygame.display.set_mode(size)
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


screen.fill(blue)
pygame.draw.rect(screen, text_wr, [0, 590, 50, 640])
pygame.display.update()


running = True
while running:

    # copying the text surface object
    # to the display surface object
    # at the center coordinate.

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
            elif event.key == pygame.K_LEFT or event.key == ord('q'):
                running = False
        elif event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill(background)

    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, blue, (250, 250), 75)

    screen.blit(text, textRect)
    # Flip the display
    pygame.display.flip()

pygame.quit()