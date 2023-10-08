
import requests
import json
from datetime import datetime, timedelta

payload = {"X-TBA-Auth-Key": "oPNFx7AbOTMJh8iAbj8croWtYrYD8COBIRytIyVZo6te6C5iSZtAYAvb7oGV7g6X"}


event = "2023cala"

def TBAGetMatches():
    request_url = "https://www.thebluealliance.com/api/v3/" + "event/" + event + "/matches/keys"
    req = requests.get(request_url, params=payload).json()
    return req

matches = TBAGetMatches()



now = datetime.now().time()


current_time = timedelta(hours=float(now.hour),minutes=float(now.minute),seconds=float(now.second))



for match in matches:
    request_url = "https://www.thebluealliance.com/api/v3/" + "match/" + match
    req = requests.get(request_url, params=payload).json()
    
now = datetime.now().time()
finished_time = timedelta(hours=float(now.hour),minutes=float(now.minute),seconds=float(now.second))



print (finished_time - current_time)

def TBANewCustom (jsonI, *nav):
    saved_args = locals()['nav']
    for arg in saved_args:
        jsonI = jsonI[arg]
    
    return jsonI



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
