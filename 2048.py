import pygame
import random

pygame.init()

# Set up window dimensions and caption
WIDTH = 400
HEIGHT = 550
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048')

# Clock and frames per second
timer = pygame.time.Clock()
fps = 60

# Load game sounds
pygame.mixer.music.load('backsound.mp3')
pygame.mixer.music.play(-1)

# Fungsi untuk memainkan suara saat memindahkan blok
def play_move_sound():
    move_sound.play()

move_sound = pygame.mixer.Sound('move.sound.mp3')

# Load sound icons
sound_on_icon = pygame.image.load('sound_on.png')
sound_off_icon = pygame.image.load('sound_off.png')
restart_icon = pygame.image.load('restart.png')

# Resize icons
sound_on_icon = pygame.transform.scale(sound_on_icon, (32, 32))
sound_off_icon = pygame.transform.scale(sound_off_icon, (32, 32))
restart_icon = pygame.transform.scale(restart_icon, (24, 24))

# Initialize fonts
pygame.font.init()
font = pygame.font.SysFont(None, 36)

# Colors for the game
colors = {0: (211, 211, 211),
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          'light text': (249, 246, 242),
          'dark text': (119, 110, 101),
          'other': (0, 0, 0),
          'bg': (249, 246, 242)}

# Game variables initialization
board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
spawn_new = True
init_count = 0
direction = ''
score = 0
sound_on = True

# Define the restart icon position (bottom right)
restart_icon_pos = (WIDTH - restart_icon.get_width() - 10, HEIGHT - restart_icon.get_height() - 10)

# Function to draw the sound and restart icons
def draw_sound_icon():
    if sound_on:
        screen.blit(sound_on_icon, (350, 10))
    else:
        screen.blit(sound_off_icon, (350, 10))
    screen.blit(restart_icon, restart_icon_pos)

# File for storing high score
high_score_file = 'high_score.txt'

# Function to load high score from file
def load_high_score():
    try:
        with open(high_score_file, 'r') as file:
            high_score = int(file.readline().strip())
            print(f"Loaded high score: {high_score}")
            return high_score
    except FileNotFoundError:
        print("File not found, returning 0 for high score.")
        return 0
    except ValueError:
        print("Error: File contains invalid data, returning 0 for high score.")
        return 0

# Function to save high score to file
def save_high_score(score):
    try:
        with open(high_score_file, 'w') as file:
            file.write(str(score))
        print(f"Saved high score: {score}")
    except IOError:
        print(f"Error: Couldn't write high score to {high_score_file}")

# Timer variables
time_limit = 2 * 60 * 1000 
start_time = pygame.time.get_ticks()
elapsed_time = 0

# Draw game over text
def draw_over():
    pygame.draw.rect(screen, 'black', [50, 250, 300, 100], 0, 10)
    game_over_text1 = font.render('GAME OVER!', True, 'white')
    game_over_text2 = font.render('Restart!', True, 'white')
    screen.blit(game_over_text1, (130, 265))
    screen.blit(game_over_text2, (70, 305))

# Draw win text
def draw_win():
    pygame.draw.rect(screen, 'black', [50, 250, 300, 100], 0, 10)
    win_text1 = font.render('YOU WIN!', True, 'white')
    win_text2 = font.render('Try again', True, 'white')
    screen.blit(win_text1, (130, 265))
    screen.blit(win_text2, (70, 305))

# Function to handle player's move based on direction
def take_turn(direc, board):
    global score 
    merged = [[False for _ in range(4)] for _ in range(4)]
    
    if direc == 'UP':
        for j in range(4):
            for i in range(1, 4):
                if board[i][j] != 0:
                    shift = i
                    while shift > 0 and board[shift - 1][j] == 0:
                        board[shift - 1][j] = board[shift][j]
                        board[shift][j] = 0
                        shift -= 1
                    if shift > 0 and board[shift - 1][j] == board[shift][j] and not merged[shift - 1][j]:
                        board[shift - 1][j] *= 2
                        score += board[shift - 1][j]
                        board[shift][j] = 0
                        merged[shift - 1][j] = True
                        play_move_sound()

    elif direc == 'DOWN':
        for j in range(4):
            for i in range(2, -1, -1):
                if board[i][j] != 0:
                    shift = i
                    while shift < 3 and board[shift + 1][j] == 0:
                        board[shift + 1][j] = board[shift][j]
                        board[shift][j] = 0
                        shift += 1
                    if shift < 3 and board[shift + 1][j] == board[shift][j] and not merged[shift + 1][j]:
                        board[shift + 1][j] *= 2
                        score += board[shift + 1][j] 
                        board[shift][j] = 0
                        merged[shift + 1][j] = True
                        play_move_sound()

    elif direc == 'LEFT':
        for i in range(4):
            for j in range(1, 4):
                if board[i][j] != 0:
                    shift = j
                    while shift > 0 and board[i][shift - 1] == 0:
                        board[i][shift - 1] = board[i][shift]
                        board[i][shift] = 0
                        shift -= 1
                    if shift > 0 and board[i][shift - 1] == board[i][shift] and not merged[i][shift - 1]:
                        board[i][shift - 1] *= 2
                        score += board[i][shift - 1]
                        board[i][shift] = 0
                        merged[i][shift - 1] = True
                        play_move_sound()

    elif direc == 'RIGHT':
        for i in range(4):
            for j in range(2, -1, -1):
                if board[i][j] != 0:
                    shift = j
                    while shift < 3 and board[i][shift + 1] == 0:
                        board[i][shift + 1] = board[i][shift]
                        board[i][shift] = 0
                        shift += 1
                    if shift < 3 and board[i][shift + 1] == board[i][shift] and not merged[i][shift + 1]:
                        board[i][shift + 1] *= 2
                        score += board[i][shift + 1]
                        board[i][shift] = 0
                        merged[i][shift + 1] = True
                        play_move_sound()

    return board

# Function to add a new block randomly
def new_pieces(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board

# Define a color for the box background
box_color = (184,134,11)

def draw_board(high_score):
    global sound_on
    pygame.draw.rect(screen, colors['bg'], [0, 100, 400, 400], 0, 10)

    # draw score box
    pygame.draw.rect(screen, box_color, [10, 10, 140, 80], 0, 5)
    score_label = font.render(f'SCORE:', True, 'black')
    score_value = font.render(f'{score}', True, 'black')
    screen.blit(score_label, (20, 20))
    screen.blit(score_value, (20, 50))

    #draw best
    pygame.draw.rect(screen, box_color, [WIDTH // 2 + 10, 10, 120, 80], 0, 5)
    best_label = font.render(f'BEST:', True, 'black')
    best_value = font.render(f'{high_score}', True, 'black')
    screen.blit(best_label, (WIDTH // 2 + 20, 20))
    screen.blit(best_value, (WIDTH // 2 + 20, 60))

    # Draw sound icon
    draw_sound_icon()

    # Draw timer
    elapsed_time = pygame.time.get_ticks() - start_time
    minutes = (time_limit - elapsed_time) // 120000
    seconds = ((time_limit - elapsed_time) % 60000) // 1000
    time_text = font.render(f'Time: {minutes}:{seconds:02}', True, 'black')
    screen.blit(time_text, (10, 500))

    # Draw game over or win if applicable
    if game_over:
        draw_over()
        if  any(2048 in row for row in board_values):
            draw_win()
        else:
            draw_over()

# Draw the game tiles
def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 120, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 157))
                screen.blit(value_text, text_rect)

# Load high score
high_score = load_high_score()
print(f"Current high score: {high_score}")

# Main game loop
run = True
start_time = pygame.time.get_ticks()
time_limit = 300000  # 5 minutes in milliseconds
game_over = False

while run:
    timer.tick(fps)
    screen.fill(pygame.Color('#FFE4C4'))

    # Calculate elapsed time and remaining time
    elapsed_time = pygame.time.get_ticks() - start_time
    remaining_time = max(0, time_limit - elapsed_time)  # Ensure remaining_time is non-negative

    # Load high score
    high_score = load_high_score()

    # Draw game board and pieces
    draw_board(high_score)
    draw_pieces(board_values)

    # Check win condition
    if any(2048 in row for row in board_values):
        # Update high score if current time is faster
        if elapsed_time < high_score or high_score == 0:
            high_score = elapsed_time
            save_high_score(high_score)
        draw_win()
        game_over = True

    # Check game over condition
    if remaining_time <= 0:
        draw_over()
        game_over = True

    # Handle restart logic if game over
    if game_over:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                # Restart the game
                board_values = [[0 for _ in range(4)] for _ in range(4)]
                spawn_new = True
                init_count = 0
                score = 0
                direction = ''
                game_over = False
                start_time = pygame.time.get_ticks()  # Restart time
                high_score = load_high_score()  # Load high score again

    # Handle user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direction = 'UP'
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if 350 <= mouse_pos[0] <= 382 and 10 <= mouse_pos[1] <= 42:
                sound_on = not sound_on
                if sound_on:
                    pygame.mixer.music.play(-1)
                else:
                    pygame.mixer.music.stop()   
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_icon_pos[0] <= mouse_pos[0] <= restart_icon_pos[0] + restart_icon.get_width() and \
                    restart_icon_pos[1] <= mouse_pos[1] <= restart_icon_pos[1] + restart_icon.get_height():
                    # Restart the game if restart icon is clicked
                    board_values = [[0 for _ in range(4)] for _ in range(4)]
                    spawn_new = True
                    init_count = 0
                score = 0
                direction = ''
                game_over = False
                start_time = pygame.time.get_ticks()  # Restart time
                high_score = load_high_score()  # Load high score again

    # Spawn new piece or take turn
    if spawn_new or init_count < 2:
        board_values = new_pieces(board_values)
        spawn_new = False
        init_count += 1

    if direction != '':
        board_values = take_turn(direction, board_values)
        direction = ''
        spawn_new = True

    pygame.display.flip()

pygame.quit()
