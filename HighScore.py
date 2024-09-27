import sqlite3
import pygame

import os

class Scores:

    dis=pygame.display.set_mode((dis_width, dis_height))
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