import requests
import json
from lxml import html, etree
from bs4 import BeautifulSoup

class Boxscore(object):
    def __init__(self, link, properties):
        self.properties = properties
        self.link = link

    def getGameStats(self, tree, playerFields, goalieFields, vteamShort, hteamShort):
        #players
        vteamtr = tree.xpath('//*[@id="'+vteamShort+'_skaters"]/tbody/tr')
        hteamtr = tree.xpath('//*[@id="'+hteamShort+'_skaters"]/tbody/tr')
        vplayerstats = self.getTeamPlayerStats(vteamtr, playerFields)
        hplayerstats = self.getTeamPlayerStats(hteamtr, playerFields)
        #goalies
        vteam_g_tr = tree.xpath('//*[@id="'+vteamShort+'_goalies"]/tbody/tr')
        hteam_g_tr = tree.xpath('//*[@id="'+hteamShort+'_goalies"]/tbody/tr')
        vgoaliestats = self.getTeamGoalieStats(vteam_g_tr, goalieFields)
        hgoaliestats = self.getTeamGoalieStats(hteam_g_tr, goalieFields)
        gamestats = {
            'vteam':{
                'players':vplayerstats,
                'goalies':vgoaliestats
            },
            'hteam':{
                'players':hplayerstats,
                'goalies':hgoaliestats
            }
        }
        return gamestats

    def getBoxscore(self):
        #load properties
        playerFields = self.properties['playerFields']
        goalieFields = self.properties['goalieFields']
        teamMapping = self.properties['teams']

        #parse website
        r = requests.get('https://www.hockey-reference.com'+self.link) #request to webpage
        allHtml = r.text
        tree = html.fromstring(allHtml) #parse results to tree
        
        #Get teams
        teams = self.getTeams(tree)
        vteam = teamMapping[teams['vteam']]
        hteam = teamMapping[teams['hteam']]

        #Get Stats
        gamestats = self.getGameStats(tree, playerFields, goalieFields, vteam, hteam)
        return gamestats
        #print json.dumps(gamestats, sort_keys=True,indent=4, separators=(',', ': '))

    def getScoreSummary(self):
        #parse website
        r = requests.get('https://www.hockey-reference.com'+self.link) #request to webpage
        allHtml = r.text
        tree = html.fromstring(allHtml) #parse results to tree

        scoringTable = tree.xpath('//*[@id="scoring"]') #get scoring table
        goals = scoringTable[0].xpath('tr')
        scores = []
        for goal in goals:
            goalDict = {}
            assists = []
            if (len(goal.xpath('td[@class="right"]')) > 0): #goal
                goalPlayers = goal.xpath('td')[2].xpath('a')
                count = 0
                for p in goalPlayers:
                    if (count == 0):
                        goalDict['scorer'] = p.text.strip()
                    else:
                        assists.append(p.text.strip())
                    count = count + 1
                goalDict['assists'] = assists
                scores.append(goalDict)
        return scores

    @staticmethod
    def getTeamPlayerStats(trlist, playerFields):
        players = []
        for tr in trlist:
            player = {}
            for field in playerFields:
                if (field == 'player'):
                    player['player'] = tr.xpath('td[@data-stat="player"][1]/a[1]')[0].text.strip()
                else:
                    player[field] = tr.xpath('td[@data-stat="'+field+'"]')[0].text.strip()
            players.append(player)
            #goals = trlist[0].xpath('td[@data-stat="goals"]')[0].text.strip()
            #print (goals)
        return players

    @staticmethod
    def getTeamGoalieStats(trlist, goalieFields):
        goalies = []
        for tr in trlist:
            goalie = {}
            for field in goalieFields:
                if (field == 'player'):
                    goalie[field] = tr.xpath('td[@data-stat="player"][1]/a[1]')[0].text.strip()
                elif (field == 'decision'):
                    if (tr.xpath('td[@data-stat="'+field+'"]')[0].text == None):
                        goalie[field] = ''
                    else:
                        goalie[field] = tr.xpath('td[@data-stat="'+field+'"]')[0].text.strip()
                else:
                    goalie[field] = tr.xpath('td[@data-stat="'+field+'"]')[0].text.strip()
            goalies.append(goalie)
        return goalies

    @staticmethod
    def getTeams(tree):
        vteam = tree.xpath('//*[@id="content"]/div[2]/div[1]/div[1]/strong/a')[0]
        hteam = tree.xpath('//*[@id="content"]/div[2]/div[2]/div[1]/strong/a')[0]
        teams = {
            'vteam':vteam.text.strip(),
            'hteam':hteam.text.strip()
        }
        return teams