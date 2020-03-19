import pymysql
import csv
import codecs
import json


db = pymysql.connect(host='127.0.0.1',user = "root", passwd="Mx!18839552597",db="DouBanMovie" ,port=3306, charset="utf8")
cursor = db.cursor()


isInt = ["cnumber"]
isList = ["alias","language","imdb","region","time","length"]
isString = ["id","name"]
isfloat=["star"]

with open("basic_info.csv","r",newline="",encoding="utf-8") as f:
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
        print("""insert ignore into movie (MovieID,name,time,length,alias,language,imdb,star,cnumber,region) values({},{},{},{},{},{},{},{},{},{})""".format(dic['id'],dic['name'],dic['time'],dic['length'],dic['alias'],dic['language'],dic['imdb'],dic['star'],dic['cnumber'],dic['region']))
        sql="""
            insert ignore into movie values({},{},{},{},{},{},{},{},{},{})""".format(dic['id'],dic['name'],dic['time'],dic['length'],dic['alias'],dic['language'],dic['imdb'],dic['star'],dic['cnumber'],dic['region'])
        cursor.execute(sql)
db.commit()
db.close()

