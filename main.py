import sys
import pygame
from src.settings import *
from src.entities.player import PLAYER
from src.entities.obstacle import OBSTACLE
from src.core.camera import Camera
from src.core.level import LEVEL

def main():
    #basic settings for game start
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Namelesscate")
    clock = pygame.time.Clock()
    running = True

    player = PLAYER(100, 100, TILE_SIZE, TILE_SIZE)
    camera = Camera()

    level = LEVEL("assets/maps/map.csv")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        player.update()

        player.is_grounded = False

        
        
        if player.vel_y >=0:
            for plat in level.platforms:
                if player.y + player.height >= plat.y and player.y < plat.y:
                    if player.x + player.width > plat.x and player.x < plat.x + plat.width:
                        player.y = plat.y - player.height
                        player.vel_y = 0
                        player.is_grounded = True
                        break
        
        camera.update(player)

        screen.fill(BG_COLOR)


        level.render(screen, camera.scroll_x)

        player.render(screen, camera.scroll_x)
    

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()