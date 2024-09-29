import pygame
import time
import random
import sqlite3
import os
from SnakeShape import draw_snake_head
from HighScore import checkHighScore, addHighScore, getHighScores

pygame.init()
pygame.mixer.init()

white = (255, 255, 255)
yellow = (255,255,102)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (50, 153, 213)

dis_width = 1200
dis_height = 800

dis=pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake game by Tijmen Rietveld')

clock = pygame.time.Clock()

snake_block = 25
snake_speed = 9

snake_List = []
Length_of_snake = 1

font_style = pygame.font.SysFont("bahnschrift", 50)
font_highscore = pygame.font.SysFont("bahnschrift", 35)
score_font = pygame.font.SysFont("comicsansms", 35)

s = 'sound'

game_over_sound = pygame.mixer.Sound(os.path.join(s, 'gameover.mp3'))

eat_sound = pygame.mixer.Sound(os.path.join(s, 'food.mp3'))

music = pygame.mixer.music.load(os.path.join(s, 'music.mp3'))

MENU = "menu"
GAME = "game"
GAME_OVER = "game_over"
QUIT = "quit"
state = MENU

def draw_button(text, x, y, w, h, inactive_color, active_color):
    """
    Draws a button on the screen and detects clicks.
    
    :param text: Text to display on the button
    :param x: X coordinate of the button
    :param y: Y coordinate of the button
    :param w: Width of the button
    :param h: Height of the button
    :param inactive_color: Button color when not hovered
    :param active_color: Button color when hovered
    :param action: Action to perform on click (can be a function or state change)
    """
    mouse = pygame.mouse.get_pos()  # Get current mouse position
    click = pygame.mouse.get_pressed()  # Get mouse clicks (returns tuple of (left, middle, right))

    # Check if mouse is over the button (hover effect)
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(dis, active_color, (x, y, w, h))  # Hover color
        if click[0] == 1:  # Check if left mouse button is clicked
            return True  # Return the action/state if clicked
    else:
        pygame.draw.rect(dis, inactive_color, (x, y, w, h))  # Default color

    # Button text
    small_text = pygame.font.SysFont("bahnschrift", 35)
    text_surf = small_text.render(text, True, white)
    dis.blit(text_surf, (x + (w / 2 - text_surf.get_width() / 2), y + (h / 2 - text_surf.get_height() / 2)))

    return None

def Score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])


def getPlayerName(current_score):
    player_name = ""
    input_active = True
    font = pygame.font.SysFont("bahnschrift", 35)  # Font for displaying name
    small_font = pygame.font.SysFont("bahnschrift", 25)  # Font for displaying high scores

    # Fetch the top 5 high scores
    conn = sqlite3.connect("Database.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT Name, Score FROM HIGHSCORE ORDER BY Score DESC LIMIT 5''')
    highscores = cursor.fetchall()
    conn.close()

    # Insert the player's current score into the list in the correct position
    inserted = False
    player_index = None  # Track the index where the player's score is inserted
    for i, (_, score) in enumerate(highscores):
        if current_score > score:
            highscores.insert(i, ("Your Name", current_score))  # Temporary placeholder for the player's name
            inserted = True
            player_index = i  # Track where we inserted the player's score
            break
    if not inserted:
        highscores.append(("Your Name", current_score))
        player_index = len(highscores) - 1  # Player's score is at the last position

    highscores = highscores[:5]


    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter key to finish input
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:  # Handle backspace
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode  # Add typed character to name

        dis.fill(blue)  # Fill the screen with background color
        message_Highscore("Congratulations! Enter your name:", green)

        # Render and display the player name on the screen
        name_surface = font.render(player_name, True, yellow)
        dis.blit(name_surface, (dis_width // 3, dis_height // 2))

         # Update the high score entry at the player's index with the current name
        if player_index is not None:
            highscores[player_index] = (player_name if player_name else "Your Name", current_score)

        # Display the top 5 high scores below the name input field
        y_offset = dis_height // 2 + 50  # Start displaying below name input
        dis.blit(small_font.render("Top 5 High Scores:", True, white), (dis_width // 3, y_offset))
        y_offset += 30

        for idx, (name, score) in enumerate(highscores):
            highscore_text = f"{idx + 1}. {name}: {score}"
            highscore_surface = small_font.render(highscore_text, True, yellow)
            dis.blit(highscore_surface, (dis_width // 3, y_offset))
            y_offset += 30  # Add space for the next high score

        pygame.display.update()

    return player_name



    

def our_snake(snake_block, snake_list, direction):
    head = snake_list[-1]

    draw_snake_head(dis, head[0], head[1], snake_block, direction)

    for x in snake_list[:-1]:
        pygame.draw.rect( dis, green, [x[0], x[1], snake_block, snake_block])


def message(msg,color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width/6, dis_height/3])

def message_Highscore(msg,color):
    mesg = font_highscore.render(msg, True, color)
    dis.blit(mesg, [dis_width/3.5, dis_height/3])

def menuLoop():
    menu = True
    font = pygame.font.SysFont("bahnschrift", 55)

    while menu == True:
        dis.fill(blue)

        title_text = font.render("Snake Game", True, white)
        title_width = title_text.get_width()
        title_height = title_text.get_height()

        # Calculate the position to center the title on the screen
        title_x = (dis_width // 2) - (title_width // 2)
        title_y = (dis_height // 3) - (title_height // 2)

        # Draw the title in the center
        dis.blit(title_text, (title_x, title_y))
        # dis.blit(title, (dis_width // 3, dis_height // 3 - 50))

         # Button dimensions
        button_width = 200
        button_height = 50

        # Calculate the position for the buttons to be centered under the title
        start_button_x = (dis_width // 2) - (button_width // 2)
        start_button_y = title_y + title_height + 50  # Spacing below the title

        quit_button_x = start_button_x
        quit_button_y = start_button_y + button_height + 20  # Spacing between buttons
        
        # Create buttons using the draw_button function
        start_action = draw_button("Start Game", start_button_x, start_button_y, 200, 50, black, green)
        quit_action = draw_button("Quit Game", quit_button_x, quit_button_y, 200, 50, black, red)

        #  dis.blit(instructions_surface, (dis_width // 3, dis_height // 3 + 150))

        if start_action:
            return GAME
        if quit_action:
            return QUIT

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

                    
                    
def gameOver():
    sound_played = False 
    if not sound_played:
        pygame.mixer.Sound.play(game_over_sound)
        sound_played = True
    
    font = pygame.font.SysFont("bahnschrift", 55)
        
    while True:
        dis.fill(blue)

        title_text = font.render("You lost!", True, white)
        title_width = title_text.get_width()
        title_height = title_text.get_height()

        # Calculate the position to center the title on the screen
        title_x = (dis_width // 2) - (title_width // 2)
        title_y = (dis_height // 3) - (title_height // 2)

        # Draw the title in the center
        dis.blit(title_text, (title_x, title_y))

        # score_text = font.render(f"Score: {Length_of_snake - 1}", True, white)
        # score_width = score_text.get_width()
        # score_height = score_text.get_height()

        # score_x = (dis_width // 2) - (score_width // 2)
        # score_y = (dis_height // 3) - (score_height // 2)

        # dis.blit(score_text, (score_x, score_y + 50))

        # Button dimensions
        button_width = 200
        button_height = 50

        # Calculate the position for the buttons to be centered under the title
        start_button_x = (dis_width // 2) - (button_width // 2)
        start_button_y = title_y + title_height + 50  # Spacing below the title

        menu_button_x = start_button_x
        menu_button_y = start_button_y + button_height + 20  # Spacing between buttons
        start_button_x, start_button_y,
        # Create buttons using the draw_button function
        start_action = draw_button("Start Game", start_button_x, start_button_y, 200, 50, black, green)
        menu_action = draw_button("Menu", menu_button_x, menu_button_y, 200, 50, black, blue)


        print("Fix this---------------------------------")
        # message("Press Q-Quit or C-Play Again", red)
        Score(Length_of_snake - 1)
        pygame.display.update()

        if start_action:
            return GAME
        if menu_action:
            return MENU

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_q:
            #         return QUIT
            #     if event.key == pygame.K_c:
            #         return GAME


def gameLoop():
    
    MENU = "menu"
    GAME = "game"
    GAME_OVER = "game_over"
    QUIT = "quit"
    state = MENU

    while True:
        if state == MENU:
            print("Menu")
            state = menuLoop()
        elif state == GAME:
            state = run_game()
            print("Game")
        elif state == GAME_OVER:
            state = gameOver()
            print("game_over")
        elif state == QUIT:
            print("Quit Game")
            pygame.quit()
            quit()


def run_game():
    game_over = False
    game_close = False
    high_Score = False

    global Length_of_snake

    x1 = dis_width/2
    y1 = dis_height/2

    x1_change = 0
    y1_change = 0

    foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block

    speedUpX = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    speedUpY = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0

    direction = "RIGHT"  # Initial direction

    pygame.mixer.music.play(-1)


    while not game_over:
        

        while game_close == True and high_Score == True:
            dis.fill(blue)
            message_Highscore("Congratulations You Beat An High Score! Press C", green)
            # message("Press C-Continue To Add High Score", yellow)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        player_name = getPlayerName(Length_of_snake - 1)
                        addHighScore(Length_of_snake - 1, player_name)
                        print(f"New high score!")

                        high_Score = False

            # addHighScore(Length_of_snake - 1, "Timma")
            # print("High Score")

        while game_close == True and high_Score == False:
            return GAME_OVER

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                game_over=True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                    direction = "RIGHT"
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                    direction = "UP"
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                    direction = "DOWN"
        

        if checkHighScore(Length_of_snake - 1):
            high_Score = True

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
                
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)

        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        # pygame.draw.circle(dis, yellow, [speedUpX, speedUpY], snake_block)
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
        
        our_snake(snake_block, snake_List,direction)
        Score(Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
            Length_of_snake += 1
            pygame.mixer.Sound.play(eat_sound)
        # elif x1 == speedUpX and y1 == speedUpY:

            
        clock.tick(snake_speed)
    
    
    pygame.quit()
    quit()

    if not os.path.isfile("./Database.db"):
            database = "Database.db"
            conn = sqlite3.connect(database)
            create_tables(conn)

gameLoop()