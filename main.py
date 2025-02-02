import loader as l
keywords = [
    '總統',
    '東森 政治',
    '三立 政治',
    '公視 政治',
    'TVBS 政治',
    '華視 政治',
    '東森',
    '三立',
    '公視',
    'TVBS',
    '華視',
    '台灣 立委',
    '台灣 議員',
    '台灣 爭議',
    '台灣 大事',
    '台灣 政治'
]
if __name__ == '__main__':
    loader = l.loader(keywords)
    if False: loader.resetSql() ### will remove all tables in database and reset them
    loader.setUpSql() ### will set up database and tables
    loader.keywords2vid()
    loader.vid2Info()
    loader.info2comment()
    print("finish")