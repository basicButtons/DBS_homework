import pymysql


db = pymysql.connect(host='127.0.0.1',user = "root", passwd="Mx!18839552597",db="DouBanMovie" ,port=3306, charset="utf8")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

    # 执行sql语句
cursor.execute('''
CREATE TABLE Movie
    (
    MovieID  varCHAR(200) PRIMARY KEY,
    MovieName varCHAR(200),
    MovieRelease varchar(200),
    MovieLength  varCHAR(200),
    MovieNickName varCHAR(200),
    MovieLanguage varCHAR(200),
    IMDb varCHAR(200),
    MovieGrade FLOAT,
    Numbers INT,
    Region varCHAR(200)
    )
    ''')
cursor.execute('''
    CREATE TABLE FilmCrew
    (
    ID VARCHAR(200) ,
    name VARCHAR(200),
    type VARCHAR(200),
    PRIMARY KEY (ID,type)
    )
    ''')
cursor.execute('''
    CREATE TABLE MovieCrew
    (
    MovieID  VARCHAR(200),
    CrewID VARCHAR(200),
    PRIMARY KEY(MovieID,CrewID)
    )
    ''')
cursor.execute('''
    CREATE TABLE MType
    (
    TypeID VARCHAR(200) PRIMARY KEY,
    MovieType VARCHAR(50)
    )
    ''')
cursor.execute('''
    CREATE TABLE MovieType
    (
    MovieID  VARCHAR(200) PRIMARY KEY,
    TypeID VARCHAR(200)
    )
    ''')
db.commit()

# 关闭数据库连接
db.close()
