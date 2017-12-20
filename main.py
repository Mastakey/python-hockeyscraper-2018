from lib.Games import Games
from lib.Boxscore import Boxscore
from lib.WEBDB import WEBDB
import json
import time
import re

def insertReplace(str):
    newStr = str.replace('\'', '\'\'')
    return newStr

def insertGames(db, season, url):
    #populate games
    games = Games(url)
    games = games.getGames()

    for game in games:
        insertSQL = """
        INSERT INTO games (gamedate, hteam, vteam, link, season, isparsed)
        VALUES (
            '"""+str(game['date'])+"""',
            '"""+str(game['hteam'])+"""',
            '"""+str(game['vteam'])+"""',
            '"""+str(game['link'])+"""',
            '"""+season+"""',
            'false'
        );
        """
        id = db.insertQuery(insertSQL)

def getGames(db, season):
    selectSQL = """
    SELECT id, gamedate, hteam, vteam, link
    FROM games
    WHERE season = '"""+season+"""'
    AND isparsed = 'false'
    """
    return db.executeQueryDict(selectSQL)

def updateGameParsed(db, id):
    updateSQL = """
    UPDATE games
    SET isparsed = 'true'
    WHERE id="""+str(id)+"""
    """
    db.updateQuery(updateSQL)

def convertTimeToSeconds(time_on_ice):
    matchObj = re.match(r'(\d+):(\d+)', time_on_ice, re.M|re.I)
    #print (matchObj)
    mm = int(matchObj.group(1))
    hh = int(matchObj.group(2))
    return mm*60+hh

def insertPlayerStats(db, id, team, oppteam, playerstats, fields):
    #generate field sql
    fieldsStr = ''
    count = 1
    for field in fields:
        fieldsStr = fieldsStr + field + ','
        #if (count < len(fields)):
        #    fieldsStr = fieldsStr + ','
        #count = count + 1
    fieldsStr = fieldsStr + 'time_on_ice_s'
    #generate field values sql
    valuesStr = ''
    count = 1
    for field in fields:
        if (field == 'time_on_ice' or field == 'player'):
            valuesStr = valuesStr + '\'' + insertReplace(str(playerstats[field])) + '\'' + ','
        else:
            valuesStr = valuesStr + str(playerstats[field]) + ','
        #if (count < len(fields)):
        #    valuesStr = valuesStr + ','
        #count = count + 1
    time_on_ice_s = convertTimeToSeconds(playerstats['time_on_ice'])
    valuesStr = valuesStr + str(time_on_ice_s)
    insertSQL = """
    INSERT INTO boxscore_player_data
    (game, team, oppteam, """+fieldsStr+""")
    VALUES (
        """+str(id)+""",
        '"""+team+"""',
        '"""+oppteam+"""',
        """+valuesStr+"""
    )
    """
    return db.insertQuery(insertSQL)

def insertGoalieStats(db, id, team, oppteam, goaliestats, fields):
    #generate field sql
    fieldsStr = ''
    count = 1
    for field in fields:
        fieldsStr = fieldsStr + field + ','
    fieldsStr = fieldsStr + 'time_on_ice_s'
    #generate field values sql
    valuesStr = ''
    count = 1
    for field in fields:
        if (goaliestats[field] == ''):
            goaliestats[field] = 0
        if (field == 'time_on_ice' or field == 'player' or field == 'decision'):
            valuesStr = valuesStr + '\'' + insertReplace(str(goaliestats[field])) + '\'' + ','
        else:
            valuesStr = valuesStr + str(goaliestats[field]) + ','
    time_on_ice_s = convertTimeToSeconds(goaliestats['time_on_ice'])
    valuesStr = valuesStr + str(time_on_ice_s)
    insertSQL = """
    INSERT INTO boxscore_goalie_data
    (game, team, oppteam, """+fieldsStr+""")
    VALUES (
        """+str(id)+""",
        '"""+team+"""',
        '"""+oppteam+"""',
        """+valuesStr+"""
    )
    """
    return db.insertQuery(insertSQL)

def main():
    #db config
    dbfile = 'db/nhldata.db'
    myDB = WEBDB(dbfile, {'logging':'on', 'type':'sqlite'})

    #parser properites config
    f = open('properties.json', 'r')
    props = json.loads(f.read())
    playerfields = props['playerFields']
    goaliefields = props['goalieFields']

    #get all unparsed games
    games = getGames(myDB, '2018')
    for game in games:
        id = game['id']
        link = game['link']
        vteam = game['vteam']
        hteam = game['hteam']
        print (link)
        stats = Boxscore(link, props).getBoxscore()

        vplayers = stats['vteam']['players']
        hplayers = stats['hteam']['players']

        vgoalies = stats['vteam']['goalies']
        hgoalies = stats['hteam']['goalies']

        for vplayer in vplayers:
            insertPlayerStats(myDB, id, vteam, hteam, vplayer, playerfields)
        for hplayer in hplayers:
            insertPlayerStats(myDB, id, hteam, vteam, hplayer, playerfields)

        for vgoalie in vgoalies:
            insertGoalieStats(myDB, id, vteam, hteam, vgoalie, goaliefields)
        for hgoalie in hgoalies:
            insertGoalieStats(myDB, id, hteam, vteam, hgoalie, goaliefields)
        updateGameParsed(myDB, id)
        time.sleep(2)
main()