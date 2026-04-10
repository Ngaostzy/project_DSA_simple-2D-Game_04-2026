import sys
import pygame
from src.settings import *
from src.entities.player import PLAYER
from src.entities.obstacle import OBSTACLE

def main():
    #basic settings for game start
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Namelesscate")
    clock = pygame.time.Clock()
    running = True

    player = PLAYER(100, 100, TILE_SIZE, TILE_SIZE)

    ground = OBSTACLE(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        player.update()

        if player.y + player.height >= ground.y and player.vel_y > 0:
            if player.x + player.width > ground.x and player.x < ground.x + ground.width:
                player.y = ground.y - player.height 
                player.vel_y = 0

        screen.fill(BG_COLOR)
        ground.render(screen)
        player.render(screen)
    

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()