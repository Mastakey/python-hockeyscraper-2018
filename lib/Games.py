import requests
from lxml import html, etree
from bs4 import BeautifulSoup

class Games(object):
    def __init__(self, url, properties):
        self.url = url
        self.properties = properties

    def getGames(self):
        games = []
        teamMapping = self.properties['teams']
        gamesHTML = self.getGamesHTML(self.url)
        table = etree.XML(self.getPrettyData(gamesHTML))
        rows = table.xpath("tbody")[0].findall("tr")
        for row in rows:
            count = 0
            link = ''
            if (len(row.xpath("th")[0].xpath("a")) > 0):
                link = row.xpath("th")[0].xpath("a")[0].attrib['href'] #<th><a link="/boxscores/..">
                date = row.xpath("th")[0].xpath("a")[0].text.strip()
            else:
                link = ''
                date = row.xpath("th")[0].text.strip()
            homeTeam = row.xpath('td[@data-stat="home_team_name"]')[0].xpath('a')[0].text.strip()
            visitTeam = row.xpath('td[@data-stat="visitor_team_name"]')[0].xpath('a')[0].text.strip()
            game = {
                'link':link,
                'date':date,
                'hteam':teamMapping[homeTeam],
                'vteam':teamMapping[visitTeam]
            }
            games.append(game)
        return games

#STATIC METHODS:
    @staticmethod
    def getGamesHTML(url):
        r = requests.get(url) #request to webpage
        allHtml = r.text
        tree = html.fromstring(allHtml) #parse results to tree
        gamesTable = tree.xpath('//*[@id="games"]') #get game table
        gamesHtml = html.tostring(gamesTable[0]) #convert to string
        return gamesHtml

    @staticmethod
    def getPrettyData(rawData):
        mySoup = BeautifulSoup(rawData, 'html.parser')
        mySoupPretty = mySoup.prettify()
        return mySoupPretty


def test_getGames():
    games = Games('https://www.hockey-reference.com/leagues/NHL_2018_games.html')
    print games.getGames()

#test_getGames()