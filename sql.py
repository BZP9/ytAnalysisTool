import mysql.connector
import os
import csv
import pandas as pd
import datetime
sql_params = {
    "database": "personal",
    "host": "localhost",
    "user": "root",
    "password": "root",
    
}
conn = mysql.connector.connect(
        host = sql_params["host"],
        user = sql_params["user"],
        password = sql_params["password"],
        charset="utf8mb4"
)
cursor = conn.cursor()

def SetUp(database):
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database};")
    cursor.execute(f"USE {database}")
    cursor.execute(f"ALTER DATABASE {sql_params['database']} CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;")
    #set up all tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS videos (
        videoId VARCHAR(15) PRIMARY KEY,
        videoTitle TEXT NOT NULL,
        channelId TEXT NOT NULL,
        channelTitle TEXT NOT NULL
    )CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci
""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comments (
        commentId VARCHAR(255) PRIMARY KEY,
        textOriginal TEXT NOT NULL,
        authorDisplayName TEXT NOT NULL,
        videoId TEXT NOT NULL,
        publishedAt DATETIME NOT NULL
    )CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci
""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS videoInfo (
        videoId VARCHAR(15) PRIMARY KEY,
        publishedAt DATETIME NOT NULL,
        viewCount INTEGER NOT NULL,
        likeCount INTEGER NOT NULL,
        commentCount INTEGER NOT NULL
    )CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci
""")

def insert_videos(thing):
    try:
        # Using parameterized query to avoid SQL injection
        cursor.execute("""
            INSERT INTO videos (videoId, videoTitle, channelId, channelTitle)
            VALUES (%s, %s, %s, %s)
        """, (thing["videoId"], thing["videoTitle"], thing["channelId"], thing["channelTitle"]))
        
        conn.commit()  # Commit the transaction
        print(f"Inserted video: {thing['videoId']}")
    
    except mysql.connector.errors.IntegrityError:
        # Handle case where videoId already exists in the database
        print(f"Duplicate videoId: {thing['videoId']} already exists.")
    
    except mysql.connector.Error as err:
        # General MySQL error handling
        print(f"Error occurred: {err}")

def insert_comments(comment):
    try:
        cursor.execute("""
            INSERT INTO comments (commentId, textOriginal, authorDisplayName, videoId, publishedAt)
            VALUES (%s, %s, %s, %s, %s)
        """, (comment["commentId"], comment["textOriginal"], comment["authorDisplayName"], comment["videoId"], comment["publishedAt"]))
        
        conn.commit()
        print(f"Inserted comment: {comment['commentId']} for video {comment['videoId']}")
    
    except mysql.connector.errors.IntegrityError:
        print(f"Duplicate commentId: {comment['commentId']} already exists.")
    
    except mysql.connector.Error as err:
        # General MySQL error handling
        print(f"Error occurred while inserting comment {comment['commentId']}: {err}")

def insert_videoInfo(info):
    try:
        # Using parameterized query to avoid SQL injection
        cursor.execute("""
            INSERT INTO videoInfo (videoId, publishedAt, viewCount, likeCount, commentCount)
            VALUES (%s, %s, %s, %s, %s)
        """, (info["videoId"], info["publishedAt"], info["viewCount"], info["likeCount"], info["commentCount"]))
        
        conn.commit()  # Commit the transaction
        print(f"Inserted video info for video: {info['videoId']}")
    
    except mysql.connector.errors.IntegrityError:
        print(f"Duplicate videoId: {info['videoId']} already exists in videoInfo.")
    
    except mysql.connector.Error as err:
        # General MySQL error handling
        print(f"Error occurred while inserting video info for video {info['videoId']}: {err}")


if __name__ == "__main__":
    SetUp(sql_params["database"])
    insert_videos()
    insert_comments()
    insert_videoInfo()