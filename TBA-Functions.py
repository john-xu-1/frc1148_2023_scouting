
import requests
import json
from datetime import datetime, timedelta

curEvent = "2023cala"


#most functions should be a combination of TBA_AddressFetcher and TBA_Locator

#Was named TBAQuery
def TBA_AddressFetcher(path):
    request_url = "https://www.thebluealliance.com/api/v3/" + path
    payload = {"X-TBA-Auth-Key": "oPNFx7AbOTMJh8iAbj8croWtYrYD8COBIRytIyVZo6te6C5iSZtAYAvb7oGV7g6X"}
    req = requests.get(request_url, params=payload).json()
    return req

#Was named TBACustom
def TBA_Locator (jsonI, *nav):
    saved_args = locals()['nav']
    for arg in saved_args:
        jsonI = jsonI[arg]
    
    return jsonI

def TBA_GetMatches(event):
    return TBA_AddressFetcher("event/" + event + "/matches/keys")

def TBA_EventTeamsFormatted (event):
    teams = TBA_AddressFetcher("event/"+event+"/teams/keys")
    for i in range (len(teams)):
        teams[i] = teams[i][3:len(teams[i]):1]
    return teams

def TBA_EventTeamsRaw (event):
    return(TBA_AddressFetcher("event/"+event+"/teams/keys"))

def TBA_TeamEventStatus(team,event):
    return TBA_AddressFetcher("team/frc"+team+"/event/"+event+"/status")


#return JSON.parse(TBAQuery('team/frc'+team+'/event/'+event+'/status'))
print (json.dumps( TBA_TeamEventStatus( TBA_EventTeamsFormatted(curEvent)[0],curEvent ),indent=2))


#fills entire sheet
def fill_matchdata():   
    matches = TBA_GetMatches() 
    now = datetime.now().time()
    current_time = timedelta(hours=float(now.hour),minutes=float(now.minute),seconds=float(now.second))

    for match in matches:
        cur_match_data= TBA_AddressFetcher("match/" + match)
        #we have the mathc data now, we fill in each match with the data, code not implemented yet
        
    now = datetime.now().time()
    finished_time = timedelta(hours=float(now.hour),minutes=float(now.minute),seconds=float(now.second))
    print (finished_time - current_time)



# function TBANewCustom(jsonI, nav) {
#   var json
#   try {
#   json = JSON.parse(jsonI)
#   } catch (err) {return ("There was an error retrieving the JSON.")}
#   try {
#   var args = Array.prototype.slice.call(arguments, 1);
#   for (var a in args) {
#     json = json[args[a]]
#   }
#   return JSON.stringify(json)
#   } catch (err) {return ("There was an error parsing the JSON.")}
# }

#print (json.dumps(req, indent=2))
# red_score = req['score_breakdown']['red']['autoPoints']
# print (red_score)




#print (TBANewCustom(req,'score_breakdown','red','autoPoints'))
