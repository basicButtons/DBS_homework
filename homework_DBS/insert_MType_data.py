import pymysql
import csv
import codecs
import json


db = pymysql.connect(host='127.0.0.1',user = "root", passwd="Mx!18839552597",db="DouBanMovie" ,port=3306, charset="utf8")
cursor = db.cursor()


isInt = ["count","type"]
isList = ["alias","language","imdb","region","time","length"]
isString = ["id","name","movietype"]
isfloat=["star"]

with open("type.csv","r",newline="",encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    for line in reader:
        dic = {}
        for i in range(len(header)):
            value = line[i]
            key = header[i]
            value = value.replace('"',  '-')
            if key in isString:
                dic[key] = '"' + value + '"'
            
            elif key in isfloat:
                if len(value) > 0 :
                    dic[key] = float(value)
                else:
                    dic[key] = 0.0
            elif key in isInt:
                if len(value) > 0 :
                    dic[key] = int(value)
                else:
                    dic[key] = 0
            else:
                dic[key] = '"' + value + '"'
        print(dic)
        print('''insert ignore into Mtype (ID,name,type) values({},{})'''.format(dic[header[0]],dic[header[1]]))
        sql='''insert ignore into Movietype  values({},{})'''.format(dic[header[0]],dic[header[1]])
        cursor.execute(sql)

db.commit()
db.close()

