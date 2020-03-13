import pygame
from reference import *
from entities.strafeentity import StrafeEntity

pygame.init()

win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

strafe_entity = StrafeEntity((WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

running = True
while running:
    clock.tick(60)
    pygame.display.set_caption(str(clock.get_fps()))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mouse Movement
    mouse_pos = pygame.mouse.get_pos()
    mouse_dpos = [WINDOW_WIDTH/2 - mouse_pos[0], WINDOW_HEIGHT/2 - mouse_pos[1]]
    strafe_entity.angle += mouse_dpos[0]

    pygame.mouse.set_pos(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)

    # Player Movement
    strafe_entity.check_jump()
    strafe_entity.move()

    win.fill(0)
    strafe_entity.draw(win)
    pygame.display.flip()
