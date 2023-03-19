import pygame, sys, random, asyncio
from pygame import *
async def main():
    # Dificulty
    # Easy      ->  10
    # Medium    ->  25
    # Hard      ->  40
    # Very Hard    ->  60
    # Impossible->  120

    dificulty = 20

    # Tamaño de la pantalla
    frame_size_x = 1600
    frame_size_y = 950

    pygame.init()
    pygame.mixer.init()

    pygame.mixer.music.load('cobra.mp3')
    pygame.mixer.music.play()

    # Creacion de la pantalla
    pygame.display.set_caption('La cobra takataka')
    game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

    # Colores, comida y snake
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)
    blue = pygame.Color(0, 0, 255)
    yellow = pygame.Color(255,255,0)
    morado = pygame.Color(128, 0, 128)
    hack_color = pygame.Color(5,5,5)

    fps_controller = pygame.time.Clock()

    snake_pos = [100, 50]
    snake_body = [[100, 50], [100-10, 50], [100-(3*10), 50]]

    green_food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    green_food_spawn = True
    red_food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    red_food_spawn = True
    randcolor_food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    randcolor_food_spawn = True

    direction = 'RIGHT'
    change_to = direction

    score = 0

    # Variables for the enemy snake
    enemy_snake_pos = [100, 50]
    enemy_snake_body = [[100, 50], [100-10, 50], [100-(3*10), 50]]

    # End Of The Game
    def game_over():
        my_font = pygame.font.SysFont('times new roman', 90)
        game_over_surface = my_font.render('Para jugar vuelve a iniciarlo', True, red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
        game_window.fill(black)
        game_window.blit(game_over_surface, game_over_rect)
        show_score(0, red, 'times', 20)
        pygame.display.flip()
        pygame.quit()
        sys.exit()

    def winner():
        my_font = pygame.font.SysFont('times new roman', 90)
        win_surface = my_font.render('Has ganado, bien jugado. Pulsa ESC', True, green)
        win_rect = win_surface.get_rect()
        win_rect.midtop = (frame_size_x/2, frame_size_y/4)
        game_window.fill(black)
        game_window.blit(win_surface, win_rect)
        show_score(0, blue, 'times', 20)
        pygame.display.flip()

    # Points
    def show_score(choice, white, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Puntos : ' + str(score), True, white)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (frame_size_x/10, 15)
        else:
            score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
        game_window.blit(score_surface, score_rect)

    #Game Loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                if event.key == pygame.K_p:
                    dificulty = 0.5 

                #Cheats
                if event.key == pygame.K_PLUS: 
                    dificulty += 5
                if event.key == pygame.K_MINUS: 
                    dificulty -= 5
                if event.key == pygame.K_F1: 
                    score += 999
                    fps_controller.tick(0.8)
                if event.key == pygame.K_F2: 
                    score += 25
                if event.key == pygame.K_F3: 
                    score += 1
                    pygame.mixer.music.stop()

        # Prohibition for the opposite movement
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Move
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        #Creation of snake and food
        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == green_food_pos[0] and snake_pos[1] == green_food_pos[1]:
            score += 1
            green_food_spawn = False
        elif snake_pos[0] == red_food_pos[0] and snake_pos[1] == red_food_pos[1]:
            score += 25
            dificulty += 3
            red_food_spawn = False
            pygame.mixer.music.load('pinsles.mp3')
            pygame.mixer.music.play()
        elif snake_pos[0] == randcolor_food_pos[0] and snake_pos[1] == randcolor_food_pos[1]:
            score += 250
            dificulty += 30
            randcolor_food_spawn = False
        else:
            snake_body.pop()

        if not green_food_spawn:
            green_food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
            green_food_spawn = True

        if not red_food_spawn:
            red_food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
            red_food_spawn = True

        if not randcolor_food_spawn:
            red_food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
            red_food_spawn = True

        game_window.fill(black)
        for pos in snake_body:

            snake = pygame.draw.rect(game_window, blue, pygame.Rect(pos[0], pos[1], 11, 11))
            green_food = pygame.draw.circle(game_window, green, (green_food_pos[0]+7, green_food_pos[1]+7), 7)
            hack_food = pygame.draw.circle(game_window, hack_color, (randcolor_food_pos[0]+7, randcolor_food_pos[1]+7), 7)
            red_food = pygame.draw.circle(game_window, red, (red_food_pos[0]+7, red_food_pos[1]+7), 7)

        if snake_pos[0] < 0 :
            snake_pos[0] = frame_size_x-10
        if snake_pos[0] > frame_size_x-10:
            snake_pos[0] = 0
        
        if snake_pos[1] < 0 :
            snake_pos[1] = frame_size_y-10
        if snake_pos[1] > frame_size_y-10:
            snake_pos[1] = 0

        for block in snake_body[1:]:
            if snake_pos[1] == block[0] and snake_pos[0] == block[1]:
                game_over()
        
        if score >= 25:
            border_up = pygame.draw.rect(game_window, yellow, pygame.Rect(0,0, 1600, 15))
            border_bottom = pygame.draw.rect(game_window, yellow, pygame.Rect(0,930, 1600, 15))
            border_left = pygame.draw.rect(game_window, yellow, pygame.Rect(0,0, 15, 930))
            border_right = pygame.draw.rect(game_window, yellow, pygame.Rect(1585,0, 15, 930))

        if score >= 50:
            def show_score(choice, white, font, size):
                score_font = pygame.font.SysFont(font, size)
                score_surface = score_font.render('Puntos : ' + str(score), True, white)
                score_rect = score_surface.get_rect()
                score_rect.midtop = (frame_size_x/10, 15)
                score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
                game_window.blit(score_surface, score_rect)
            
            border_up = pygame.draw.rect(game_window, yellow, pygame.Rect(0,0, 1600, 50))
            border_bottom = pygame.draw.rect(game_window, yellow, pygame.Rect(0,900, 1600, 50))
            border_left = pygame.draw.rect(game_window, yellow, pygame.Rect(0,0, 50, 930))
            border_right = pygame.draw.rect(game_window, yellow, pygame.Rect(1550,0, 50, 900))

            if snake_pos[0] < 15 :
                snake_pos[0] = frame_size_x-15
            if snake_pos[0] > frame_size_x-15:
                snake_pos[0] = 15
            
            if snake_pos[1] < 40 :
                snake_pos[1] = frame_size_y-110
            if snake_pos[1] > frame_size_y-60:
                snake_pos[1] = 30
        
        if score >= 150:
            border_up = pygame.draw.rect(game_window, yellow, pygame.Rect(0,0, 1600, 100))
            border_bottom = pygame.draw.rect(game_window, yellow, pygame.Rect(0,800, 1600, 100))
            border_left = pygame.draw.rect(game_window, yellow, pygame.Rect(0,0, 100, 930))
            border_right = pygame.draw.rect(game_window, yellow, pygame.Rect(1500,0, 100, 900))
            
        if score >= 200:
            enemy_snake_body.insert(0, list(enemy_snake_pos))
            for pos in enemy_snake_body:
                enemy_snake = pygame.draw.rect(game_window, morado, pygame.Rect(pos[0], pos[1], 14, 14))
            
            directions = ["ARRIBA", "ABAJO", "IZQUIERDA", "DERECHA"]
            change_to = random.choice(directions)
            if change_to == 'ARRIBA':
                enemy_snake_pos[1] -= 10
            elif change_to == 'ABAJO':
                enemy_snake_pos[1] += 10
            elif change_to == 'IZQUIERDA':
                enemy_snake_pos[0] -= 10
            elif change_to == 'DERECHA':
                enemy_snake_pos[0] += 10
            
            if enemy_snake_pos[0] < 0 :
                enemy_snake_pos[0] = frame_size_x-10
            if enemy_snake_pos[0] > frame_size_x-10:
                enemy_snake_pos[0] = 350
            
            if enemy_snake_pos[1] < 0 :
                enemy_snake_pos[1] = frame_size_y-10
            if enemy_snake_pos[1] > frame_size_y-10:
                enemy_snake_pos[1] = 350
            
            change_to = random.choice(directions)

        if score >= 350:
            border_up = pygame.draw.rect(game_window, red, pygame.Rect(0,0, 1600, 200))
            border_bottom = pygame.draw.rect(game_window, red, pygame.Rect(0,800, 1600, 250))
            border_left = pygame.draw.rect(game_window, red, pygame.Rect(0,0, 250, 930))
            border_right = pygame.draw.rect(game_window, red, pygame.Rect(1350,0, 250, 900))
            if snake_pos[0] >= 1350 or snake_pos[0] < 250 or snake_pos[1] >= 800 or snake_pos[1] < 200:
                game_over()

        if score >= 600:
            winner()
            
        show_score(1, white, 'consolas', 20)
        pygame.display.update()
        
        # The speed of the game refers to the difficulty of the game, if the difficulty is easy it will work at 10 FPS. Which is referenced at the beginning of the codeo
        fps_controller.tick(dificulty)
        await asyncio.sleep(0)
asyncio.run(main())