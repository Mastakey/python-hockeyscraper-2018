from lib.Games import Games
from lib.WEBDB import WEBDB
import json
import time

def insertGames(db, season, url, props):
    #populate games
    games = Games(url, props)
    games = games.getGames()

    for game in games:
        getGameSQL = """
        SELECT id, link 
        FROM games
        WHERE gamedate = '"""+game['date']+"""'
        AND hteam = '"""+game['hteam']+"""'
        AND vteam = '"""+game['vteam']+"""'
        """
        results = db.executeQueryDict(getGameSQL)
        id = 0
        link = ''

        insertSQL = """
        INSERT INTO games (gamedate, hteam, vteam, link, season, isparsed)
        VALUES (
            '"""+str(game['date'])+"""',
            '"""+str(game['hteam'])+"""',
            '"""+str(game['vteam'])+"""',
            '"""+str(game['link'])+"""',
            '"""+str(season)+"""',
            'false'
        );
        """

        if (len(results) > 0):
            id = results[0]['id']
            link = results[0]['link']
            if (link == ''):
                updateSQL = """
                UPDATE games
                SET link = '"""+game['link']+"""'
                WHERE id="""+str(id)+"""
                """
                db.updateQuery(updateSQL)
        else:
            id = db.insertQuery(insertSQL)
        

def main():
    #db config
    dbfile = 'db/nhldata.db'
    myDB = WEBDB(dbfile, {'logging':'on', 'type':'sqlite'})
    #parser properites config
    f = open('properties.json', 'r')
    props = json.loads(f.read())
    #insertGames only needs to be run once a season to load all games
    insertGames(myDB, '2018', 'https://www.hockey-reference.com/leagues/NHL_2018_games.html', props)
main()