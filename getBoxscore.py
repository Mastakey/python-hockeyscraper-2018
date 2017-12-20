from lib.Boxscore import Boxscore
import json
def main():
    #parser properites config
    f = open('properties.json', 'r')
    props = json.loads(f.read())
    playerfields = props['playerFields']
    goaliefields = props['goalieFields']

    link = '/boxscores/201710040WPG.html'

    stats = Boxscore(link, props).getBoxscore()
    print (stats)
    
main()