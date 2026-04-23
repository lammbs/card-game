import random
import pygame

pygame.init()
window = pygame.display.set_mode((1000,500), pygame.RESIZABLE)
pygame.display.set_caption("Jackass")



run = True
while run:
    pygame.time.delay(60)

    window.fill((43, 130, 57))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


        pygame.display.update()

pygame.quit()
