import cProfile
import pstats
import io
import pygame
from main import Game 
import random
from src.entities.enemies.patrol_enemy import PATROL_ENEMY

def run_stress_test():
    """Hàm chạy game giả lập với số lượng Entity khổng lồ"""
    pygame.init()
    test_game = Game(level_path="assets/maps/benchmark_map.ldtk") 
    test_game.reset_game()
    
    print("[BENCHMARK] Đang spawn 400 con quái vật...")
    
    map_width = test_game.level.width
    map_height = test_game.level.height

    for i in range(250):
        random_x = random.randint(64, map_width - 64)
        random_y = random.randint(64, map_height // 2) 
        new_enemy = PATROL_ENEMY(x=random_x, y=random_y, width=32, height=32)
        test_game.enemies.append(new_enemy)

    print("[BENCHMARK] Bắt đầu đo lường 600 khung hình (10 giây)...")
    
    frames_to_test = 600

    for _ in range(frames_to_test):
        test_game.update()
        test_game.render()

    pygame.quit()

def main():
    pr = cProfile.Profile()
    pr.enable() 
    
    run_stress_test()
    
    pr.disable() 
    
    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    
    print("\n" + "="*50)
    print(" BÁO CÁO HIỆU NĂNG CPU (PROFILING REPORT) ")
    print("="*50)
    
    ps.print_stats(20) 
    print(s.getvalue())

if __name__ == "__main__":
    main()