import pymysql
import json

db = pymysql.connect(host='127.0.0.1',user = "root", passwd="。。。。。",db="DouBanMovie" ,port=3306, charset="utf8")
cursor = db.cursor()

HEAD = ['']
def getRes(sql):
    cursor.execute(sql)
    return cursor.fetchall()


def getDetailById(id):
    sql1 = '''
    select MovieName,MovieRelease,MovieLength,MovieNickName,MovieLanguage,IMDB,MovieGrade,Numbers,Region
    from Movie
    where MovieID = {}
    '''.format(id)
    res1 = getRes(sql1) 
    res2 = getCrewFormMovieID(id) # 0:导演，1:编剧，2:主演
    res3 = getTypeFromID(id)
    res = []
    for i in res1[0]:
        res.append(i)
    res.append(getCrewFormMovieID(id)['director'])
    res.append(getCrewFormMovieID(id)['editor'])
    res.append(getCrewFormMovieID(id)['actor'])
    res.append(getTypeFromID(id))
    return {'id': id, 'name': res[0], 'time': res[1], 'length': res[2], 'alias': res[3], 'language': res[4],
    'imdb':res[5],'star':res[6],'number':res[7],'region':res[8],'director':res[9],'editor':res[10],'actor':res[11],'type':res[12]}


def movieMetailList_hot(page=1, pagesize=10):
    offset = (page - 1) * pagesize
    sql = '''
    select MovieID,MovieName,MovieLanguage,MovieGrade,Region
    from Movie
    ORDER BY Movie.Numbers desc
    limit {},{};
    '''.format(offset, pagesize)
    resList = getRes(sql)
    for res in resList:
        id = res[0]
        crew = getCrewFormMovieID(id)
        mtype = getTypeFromID(id)
        response = dict(
            {'id': id, 'name': res[1], 'star': res[3], 'region': res[4], 'type': mtype, 'language': res[2]}, **crew)
    return response


def getSomeDetails(id):
    id  = '"'+id+'"'
    sql = '''
    select MovieID,MovieName,MovieLanguage,MovieGrade,Region
    from Movie
    where MovieID = {}
    '''.format(id)
    res = getRes(sql)
    id = res[0]
    crew = getCrewFormMovieID(id)
    mtype = getTypeFromID(id)
    response.append(dict({'id': id, 'name': res[1], 'star': res[3], 'region': res[4], 'type': mtype, 'language': res[2]}, **crew))
    sql1 = '''
    select MovieID
    from Movie
    '''
    total = cursor.execute(sql1)
    return {'total': total, 'list': response}


def movieMetailList_star(page=1, pagesize=10):
    response = []
    offset = (page - 1) * pagesize
    sql = '''
    select MovieID,MovieName,MovieLanguage,MovieGrade,Region
    from Movie
    ORDER BY Movie.MovieGrade desc
    limit {},{};
    '''.format(offset, pagesize)
    resList = getRes(sql)
    for res in resList:
        id = res[0]
        crew = getCrewFormMovieID(id)
        mtype = getTypeFromID(id)
        response.append(dict(
            {'id': id, 'name': res[1], 'star': res[3], 'region': res[4], 'type': mtype, 'language': res[2]}, **crew))
    sql = '''
    select MovieID
    from Movie
    '''
    total = cursor.execute(sql)
    return {'total': total, 'list': response}   

def getTypeFromID(id):
    sql = '''
    select TypeID
    from  MovieType
    where MovieType.MovieID = {}
    '''.format(id)
    types = getRes(sql)
    res = ""
    for mtype in types:
        res += mtype[0] + ", "
    return res


def getCrewFormMovieID(id):
    sql = '''
    select Name, Type
    from FilmCrew, MovieCrew
    where FilmCrew.ID = MovieCrew.CrewID and MovieCrew.MovieID = {}
    '''.format(id)

    crews = getRes(sql)
    director = ""
    editor = ""
    actor = ""
    for crew in crews:
        if crew[1] == '0':
            director += crew[0] 
        elif crew[1] == '1':
            editor += crew[0] + " / " 
        else:
            actor += crew[0] + " / " 
    return {'director' : director, 'editor' : editor, 'actor' : actor}

def searchByNameAndType(dic):
    if dic['name'] != None and dic['type'] != None:
        Name = dic['name']
        Type = dic['type']
    elif dic['name'] != None and dic['type'] == None:
        Name = dic['name']
        Type = ''
    elif dic['name'] == None and dic['type'] != None:
        Name = ''
        Type = dic['type']
    a = ''
    for i in Name:
        a += '%'+ i
    a += '%'
    a = '"'+a+'"'
    sql1 = '''
    select MovieID 
    from Movie
    where MovieName like {}
    '''.format(a)

    idres1 = getRes(sql1)

    Type= '"'+ Type+ '"'
    sql2 = '''
    select MovieID
    from MovieType
    where TypeID = {}
    '''.format(Type)

    idres2 = getRes(sql2)
    idres = []
    if dic['name'] != None and dic['type'] != None:
        idres = list(set(idres1) ^ set(idres2))
    elif dic['name'] == None and dic['type'] != None:
        idres = idres2
    elif dic['name'] != None and dic['type'] == None:
        idres = idres1
    res=[]


    for id in idres:
        id = '"'+id[0]+'"'
        tempDic = getDetailById(id)
        res.append(tempDic)
        Dic = res
    return {'total': len(idres), 'list': Dic}

def getCrewIdFromFlimCrew(name):
    name = '"'+ name +'"'
    new =''
    for i in name:
        new += "%" + i
    new = '"' + new + "%" +'"'
    sql = '''
        SELECT ID
        FROM FilmCrew
        where name like {}
        '''.format(new)
    res = getRes(sql)[0][0]
    return res

def getInfoFromCrewId(id):
    id = '"'+ str(id) +'"'
    sql1='''
    SELECT Name
    FROM FilmCrew
    WHERE ID={}
    '''.format(id)
    name = getRes(sql1)[0][0]
    
    sql2 = '''
    SELECT AVG(MovieGrade)
    FROM Movie
    WHERE MovieID in 
	(SELECT distinct MovieID
	FROM MovieCrew
	WHERE CrewID={})
    '''.format(id)
    star = getRes(sql2)[0][0]


    sql3 = '''
    SELECT COUNT(*)
    FROM Movie
    WHERE MovieID in
	(SELECT MovieID
	FROM MovieCrew
	WHERE CrewID={})
    '''.format(id)
    number = getRes(sql3)[0][0]

    sql4 = '''
    SELECT MovieName
    FROM Movie
    WHERE MovieID in
	(SELECT MovieID
	FROM MovieCrew
	WHERE CrewID={})
    ORDER BY Numbers DESC
    limit 5
    '''.format(id)
    movie = getRes(sql4)
    movieres = ''  
    for i in movie:
        movieres += i[0] + "/"
    res = {'name':name,'star':star,'count':number,'movie':movieres} 
    return res


def updataBasicMovieInfo(dic):
    id ='"'+ dic['id']+'"'   
    name ='"'+ dic['name']+'"'
    star ='"'+ dic['star']+ '"'
    region ='"'+ dic['region']+'"'
    language ='"'+ dic['language']+'"'
    time ='"'+ dic['time']+'"'
    length ='"'+ dic['length']+ '"'
    alias ='"'+ dic['alias'] + '"'
    imdb ='"'+ dic['imdb'] + '"'
    sql = '''
    update Movie
    set
        MovieName = {},
        MovieGrade = {},
        Region = {},
        Movielanguage = {},
        MovieRelease = {},
        MovieLength = {},
        MovieNickName = {},
        IMDB = {}
    where 
        MovieID = {}
    '''.format(name,star,region,language,time,length,alias,imdb,id)
    print(sql)
    print(sql)
    cursor.execute(sql)
    db.commit()

def updataCrewBasicInfo(dic):
    name = dic['name']
    id = dic['id']
    name = '"' + name + '"'
    id = '"' + id + '"'
    sql = '''
    update FilmCrew
    set name = {}
    where id = {}
    '''.format(name,id)
