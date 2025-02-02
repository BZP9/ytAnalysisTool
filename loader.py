import mysql.connector
import os
import csv
import pandas as pd
import datetime
import sth2sth as s2s
import sth2sql as s2q

class loader():
    def __init__(self, keywords: list):
        self.keywords = keywords

    def resetSql(self):
        s2q.resetDatabase()

    def setUpSql(self):
        s2q.SetUp()

    def keywords2vid(self):
        for keyword in self.keywords:
            for vid in s2s.keyword2vid(keyword):
                s2q.insert_videos(vid)
        s2q.videosCount()
    
    def vid2Info(self):
        for vid in s2q.videoList():
            s2q.insert_videoInfo(s2s.vid2info(vid))
        s2q.videoInfoCount()

    def info2comment(self, interval = 14, minComments = 50):
        for info in s2q.videoInfoList(interval, minComments):
            for comment in s2s.vid2comment(info[0]):
                s2q.insert_comments(comment)
        s2q.commentsCount()


if __name__ == '__main__':
    # l = loader(["sth"])
    # l.sql2info2comments()
    s2q.commentsCount()
    # for info in l.sql2vid2vidInfo():
    #     print(info)
        