import pygame
import time
import random
import sqlite3
import os

pygame.init()

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

snake_head_img = pygame.image.load("snake_head1.jpg")

font_style = pygame.font.SysFont("bahnschrift", 50)
font_highscore = pygame.font.SysFont("bahnschrift", 35)
score_font = pygame.font.SysFont("comicsansms", 35)

def create_tables(conn):
    print("table made")
    db = conn
    z = db.cursor()
    z.execute(""" CREATE TABLE HIGHSCORE (
        Name VARCHAR(255) NOT NULL,
        Score INT NOT NULL
    ); """)

    db.commit()
    db.close()

def Score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])

def checkHighScore(score):

    conn = sqlite3.connect("Database.db")
    cursor = conn.cursor() 
    cursor.execute('''SELECT Score FROM HIGHSCORE ORDER BY Score DESC LIMIT 5''')
    highscores = cursor.fetchall()

    if not highscores:
        # If there's no high score yet, consider it a new high score
        return True
    for highscore in highscores:
        # print(i[0])
        if score > highscore[0]:
            return True
    
    return False
        
def getHighScores():
    conn = sqlite3.connect("Database.db")
    cursor = conn.cursor() 
    highscores=cursor.execute('''SELECT Score
                      FROM HIGHSCORE 
                      ORDER BY Score DESC 
                      LIMIT 5''') 
    return highscores
        
    


def addHighScore(score, name):
    try:
        if not os.path.isfile("./Database.db"):
            database = "Database.db"
            conn = sqlite3.connect(database)
            create_tables(conn)
        
        conn = sqlite3.connect("Database.db")
        cursor = conn.cursor()

        with conn:
            cursor.execute(" INSERT INTO HIGHSCORE VALUES(:Name, :Score)",
                           {
                               "Name": name,
                               "Score" : score
                           })

        # data=cursor.execute('''SELECT * FROM HIGHSCORE''') 
        # for row in data: 
        #     print(row) 
        
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(e)

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


def draw_snake_head(x, y, size, direction):
    # Draw the head (rounded rectangle for a more natural snake head shape)
    pygame.draw.rect(dis, green, [x, y, size, size], border_radius=size // 4)

    # Draw the eyes (larger and more centered)
    eye_size = size // 3
    eye_offset_x = size // 5
    eye_offset_y = size // 4

    # Position the eyes based on direction
    if direction == "UP" or direction == "DOWN":
        pygame.draw.circle(dis, white, (x + eye_offset_x, y + eye_offset_y), eye_size)
        pygame.draw.circle(dis, white, (x + size - eye_offset_x, y + eye_offset_y), eye_size)
    elif direction == "LEFT":
        pygame.draw.circle(dis, white, (x + eye_offset_y, y + eye_offset_x), eye_size)
        pygame.draw.circle(dis, white, (x + eye_offset_y, y + size - eye_offset_x), eye_size)
    elif direction == "RIGHT":
        pygame.draw.circle(dis, white, (x + size - eye_offset_y, y + eye_offset_x), eye_size)
        pygame.draw.circle(dis, white, (x + size - eye_offset_y, y + size - eye_offset_x), eye_size)

    # Draw pupils
    pupil_size = eye_size // 2
    if direction == "UP" or direction == "DOWN":
        pygame.draw.circle(dis, black, (x + eye_offset_x, y + eye_offset_y), pupil_size)
        pygame.draw.circle(dis, black, (x + size - eye_offset_x, y + eye_offset_y), pupil_size)
    elif direction == "LEFT":
        pygame.draw.circle(dis, black, (x + eye_offset_y, y + eye_offset_x), pupil_size)
        pygame.draw.circle(dis, black, (x + eye_offset_y, y + size - eye_offset_x), pupil_size)
    elif direction == "RIGHT":
        pygame.draw.circle(dis, black, (x + size - eye_offset_y, y + eye_offset_x), pupil_size)
        pygame.draw.circle(dis, black, (x + size - eye_offset_y, y + size - eye_offset_x), pupil_size)

    # Draw the tongue based on direction
    tongue_length = size // 1.5
    tongue_width = 3
    tongue_offset = size // 2

    if direction == "UP":
        pygame.draw.line(dis, red, (x + tongue_offset, y), (x + tongue_offset, y - tongue_length), tongue_width)
    elif direction == "DOWN":
        pygame.draw.line(dis, red, (x + tongue_offset, y + size), (x + tongue_offset, y + size + tongue_length), tongue_width)
    elif direction == "LEFT":
        pygame.draw.line(dis, red, (x, y + tongue_offset), (x - tongue_length, y + tongue_offset), tongue_width)
    elif direction == "RIGHT":
        pygame.draw.line(dis, red, (x + size, y + tongue_offset), (x + size + tongue_length, y + tongue_offset), tongue_width)
    

def our_snake(snake_block, snake_list, direction):
    head = snake_list[-1]

    draw_snake_head(head[0], head[1], snake_block, direction)

    for x in snake_list[:-1]:
        pygame.draw.rect( dis, green, [x[0], x[1], snake_block, snake_block])


def message(msg,color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width/6, dis_height/3])

def message_Highscore(msg,color):
    mesg = font_highscore.render(msg, True, color)
    dis.blit(mesg, [dis_width/3.5, dis_height/3])

def gameLoop():
    game_over = False
    game_close = False
    high_Score = False

    x1 = dis_width/2
    y1 = dis_height/2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block

    speedUpX = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    speedUpY = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0

    direction = "RIGHT"  # Initial direction


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
            dis.fill(blue)
            message("Press Q-Quit or C-Play Again", red)
            Score(Length_of_snake -1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

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
        # elif x1 == speedUpX and y1 == speedUpY:

            
        clock.tick(snake_speed)
    
    
    pygame.quit()
    quit()

if not os.path.isfile("./Database.db"):
            database = "Database.db"
            conn = sqlite3.connect(database)
            create_tables(conn)

gameLoop()