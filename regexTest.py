import re

def convertTimeToSeconds(time_on_ice):
    matchObj = re.match(r'(\d+):(\d+)', time_on_ice, re.M|re.I)
    #print (matchObj)
    mm = int(matchObj.group(1))
    hh = int(matchObj.group(2))
    return mm*60+hh

seconds = convertTimeToSeconds('33:11')
print (seconds)