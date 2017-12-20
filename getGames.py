import requests
from lxml import html, etree
from bs4 import BeautifulSoup

def getGamesHTML(url):
    r = requests.get(url) #request to webpage
    allHtml = r.text
    tree = html.fromstring(allHtml) #parse results to tree
    gamesTable = tree.xpath('//*[@id="games"]') #get game table
    gamesHtml = html.tostring(gamesTable[0]) #convert to string
    return gamesHtml

def getPrettyData(rawData):
    mySoup = BeautifulSoup(rawData, 'html.parser')
    mySoupPretty = mySoup.prettify()
    return mySoupPretty
    
def getGames(url):
    games = []
    gamesHTML = getGamesHTML(url)
    table = etree.XML(getPrettyData(gamesHTML))
    rows = table.xpath("tbody")[0].findall("tr")
    for row in rows:
        count = 0
        link = row.xpath("th")[0].xpath("a")[0].attrib['href'] #<th><a link="/boxscores/..">
        date = row.xpath("th")[0].xpath("a")[0].text.strip()
        homeTeam = row.xpath('td[@data-stat="home_team_name"]')[0].xpath('a')[0].text.strip()
        visitTeam = row.xpath('td[@data-stat="visitor_team_name"]')[0].xpath('a')[0].text.strip()
        game = {
            'link':link,
            'date':date,
            'hteam':homeTeam,
            'vteam':visitTeam
        }
        games.append(game)
        break
    return games
    
def main():
    games = getGames('https://www.hockey-reference.com/leagues/NHL_2018_games.html')
    #print len(games)
    print (games[0])

main()