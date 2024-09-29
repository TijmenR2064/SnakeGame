import sqlite3
import os

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

    

