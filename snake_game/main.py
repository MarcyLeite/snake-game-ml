import pygame, time
from Board import Board, pixel_size, board_size
from Snake import Snake
from Fruit import FruitHandler

death_count = 0
game_time = 0
FPS = 10

def run_game(choose_action = None, steps = 0):
    global death_count, game_time, FPS
    
    round_steps = 0

    pygame.init()
    surface = pygame.display.set_mode((pixel_size * board_size, pixel_size * board_size + 100))
    surface.fill((0, 0, 0))

    clock = pygame.time.Clock()

    board = None
    fruit_handler = None
    snake = None 

    def reset():
        nonlocal board, fruit_handler, snake, surface, round_steps
        round_steps = 0
        board = Board(surface)
        fruit_handler = FruitHandler(board)
        snake = Snake(board, fruit_handler)

    reset()

    running = True

    font = pygame.font.Font('freesansbold.ttf', 16)

    while running:

        fps = FPS
        if fps == 0: fps = 1

        if snake.dead:
            death_count += 1
            reset()

        str_game_time = time.strftime('%H:%M:%S', time.gmtime(game_time))

        pygame.draw.rect(surface, (93, 77, 161), pygame.Rect(0, 0, pixel_size* board_size, 100))

        time_text = font.render("Section Time: " + str_game_time, True, (255, 255, 255))
        surface.blit(time_text, pygame.Rect(10, 10, 50, 100))

        deaths_text = font.render("Section Deaths: " + str(death_count), True, (255, 255, 255))
        surface.blit(deaths_text, pygame.Rect(10, 30, 50, 100))

        steps_text = font.render("Total Steps: " + str(steps), True, (255, 255, 255))
        surface.blit(steps_text, pygame.Rect(10, 50, 50, 100))

        round_steps_text = font.render("Round Steps: " + str(round_steps), True, (255, 255, 255))
        surface.blit(round_steps_text, pygame.Rect(10, 70, 50, 100))

        fps_text = font.render("FPS: " + str(fps), True, (255, 255, 255))
        surface.blit(fps_text, pygame.Rect((pixel_size * board_size)/2 + 50, 10, 50, 100))

        if snake.dead:
            death_count += 1

        funcs = None

        if choose_action:
            state = snake.get_state()
            funcs = choose_action(state, steps)
            funcs[0](snake)

        for event in pygame.event.get():
            if not choose_action and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    snake.set_direction(1)
                elif event.key == pygame.K_RIGHT:
                    snake.set_direction(2)
                elif event.key == pygame.K_UP:
                    snake.set_direction(3)
                elif event.key == pygame.K_LEFT:
                    snake.set_direction(4)
                elif event.key == pygame.K_r:
                    reset()
                break

            if event.type == pygame.KEYDOWN:
                if event.key == 61:
                    FPS += 10
                if event.key == 45:
                    FPS -= 10
            
            if event.type == pygame.QUIT:
                running = False

        reward = snake.step()
        fruit_handler.step()
        
        if funcs:
            funcs[1](reward, snake.get_state())
            
        board.render()

        game_time += 60/fps
        steps += 1
        round_steps += 1

        clock.tick(fps)


if __name__ == '__main__':
    run_game()