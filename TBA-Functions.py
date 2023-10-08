import requests
import json

request_url = "https://www.thebluealliance.com/api/v3/" + "match/" + "2023cala_qm3"
payload = {"X-TBA-Auth-Key": "oPNFx7AbOTMJh8iAbj8croWtYrYD8COBIRytIyVZo6te6C5iSZtAYAvb7oGV7g6X"}
req = requests.get(request_url, params=payload).json()



print (json.dumps(req, indent=2))
red_score = req['score_breakdown']['red']['autoPoints']
print (red_score)
