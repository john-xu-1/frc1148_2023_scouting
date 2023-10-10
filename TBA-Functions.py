
import requests
import json
from datetime import datetime, timedelta

curEvent = "2023cala"

def prettyPrint(jsonI):
    print (json.dumps(jsonI,indent=2))


#Was named TBAQuery
def TBA_AddressFetcher(path):
    request_url = "https://www.thebluealliance.com/api/v3/" + path
    payload = {"X-TBA-Auth-Key": "oPNFx7AbOTMJh8iAbj8croWtYrYD8COBIRytIyVZo6te6C5iSZtAYAvb7oGV7g6X"}
    req = requests.get(request_url, params=payload).json()
    return req

#Was named TBANewCustom (I kind of realized this method is a bit useless)
def TBA_Locator (jsonI, *nav):
    saved_args = locals()['nav']
    for arg in saved_args:
        jsonI = jsonI[arg]
    
    return jsonI

def TBA_Status():
    return TBA_AddressFetcher('status')

def TBA_YearEvents(year):
    return TBA_AddressFetcher("events/"+str(year)+"/keys")

def TBA_MaxSeason ():
    return TBA_Status()['max_season']

#======================================Team Specific Methods======================================

def TBA_TeamEventStatus(team,event):
    return TBA_AddressFetcher("team/frc"+team+"/event/"+event+"/status")

def TBA_TeamEventMatches(team,event):
    return TBA_AddressFetcher("team/frc"+team+"/event/"+event+"/matches")

def TBA_TeamEventMatchKeys(team,event):
    return TBA_AddressFetcher("team/frc"+team+"/event/"+event+"/matches/keys")

def TBA_Social(team):
    return TBA_AddressFetcher("team/frc"+team+"/social_media")

#print (json.dumps( TBA_Social( TBA_EventTeamsFormatted(curEvent)[0]),indent=2))

def TBA_WinRate(team,event):
    status = TBA_TeamEventStatus(team,event)
    return (status["qual"]["ranking"]["record"]["wins"] + 0.5*status["qual"]["ranking"]["record"]["ties"]) / (status["qual"]["ranking"]["matches_played"]) * 100

#print (json.dumps( TBA_WinRate( TBA_EventTeamsFormatted(curEvent)[0],curEvent),indent=2))

def TBA_TeamInfo(team):
    return TBA_AddressFetcher('team/frc'+team+"/simple")

def TBA_TeamFullInfo(team):
    return TBA_AddressFetcher('team/frc'+team)

def TBA_TeamNicknname(team):
    return TBA_TeamInfo(team)['nickname']

def TBA_TeamName(team):
    return TBA_TeamInfo(team)['name']

def TBA_TeamCity(team):
    return TBA_TeamInfo(team)['city']

def TBA_TeamName(team):
    return TBA_TeamInfo(team)['state_prov']

def TBA_TeamCountry(team):
    return TBA_TeamInfo(team)['country']

def TBA_TeamSite(team):
    return TBA_TeamFullInfo(team)['website']

def TBA_TeamRookie(team):
    return TBA_TeamFullInfo(team)['rookie_year']

def TBA_TeamEventQualRank(team,event):
    return TBA_TeamEventStatus(team,event)['qual']['ranking']['rank']

def TBA_TeamEventMatchesYear(team,year):
    return TBA_AddressFetcher("team/frc"+team+"/events/"+year)

def TBA_TeamEventMatchKeysYear(team,year):
    return TBA_AddressFetcher("team/frc"+team+"/events/"+year+"/keys")

#================================================================================================  
    

#======================================Event Specific Methods======================================
def TBA_EventOPRs(event):
    return TBA_AddressFetcher("event/"+event+"/oprs")

#Get all the matches in an event
def TBA_EventMatchKeys(event):
    return TBA_AddressFetcher("event/" + event + "/matches/keys")

def TBA_EventTeamsFormatted (event):
    teams = TBA_AddressFetcher("event/"+event+"/teams/keys")
    for i in range (len(teams)):
        teams[i] = teams[i][3:len(teams[i]):1]
    return teams

def TBA_EventTeamsRaw (event):
    return(TBA_AddressFetcher("event/"+event+"/teams/keys"))

#================================================================================================


#======================================Match Specific Methods======================================

def TBA_GetCurMatch(match):
    return TBA_AddressFetcher("match/" + match)

def TBA_MatchWinner(match):
    return TBA_GetCurMatch(match)["winning_alliance"]

def OPR(team):
    return TBA_EventOPRs(event)['oprs']['frc'+team]
def DPR(team):
    return TBA_EventOPRs(event)['dprs']['frc'+team]
def CCWM(team):
    return TBA_EventOPRs(event)['ccwms']['frc'+team]
def GetMatchData(MatchKey)
    return TBA_EventMatchKeys(event)[MatchKey]
def GetBlueRP:(MatchKey)
    return GetMatchData(MatchKey)['score_breakdown']['blue']['rp']
def GetRedRP:(MatchKey)
    return GetMatchData(MatchKey)['score_breakdown']['red']['rp']
def GetBlueScore:(MatchKey)
    return GetMatchData(MatchKey)['score_breakdown']['blue']['totalPoints']
def GetRedRP:(MatchKey)
    return GetMatchData(MatchKey)['score_breakdown']['red']['totalPoints']
def GetBlueTeams #is this wrong casue returns 3 teams, how to split
    return GetMatchData(MatchKey)['alliances']['blue']['team_keys']
def GetRedTeams #is this wrong casue returns 3 teams, how to split
    return GetMatchData(MatchKey)['alliances']['red']['team_keys']
def GetBlueAutoPoints:(MatchKey)
    return GetMatchData(MatchKey)['score_breakdown']['blue']['autoPoints']
def GetRedAutoPoints:(MatchKey)
    return GetMatchData(MatchKey)['score_breakdown']['red']['autoPoints']

all the below need:
returnGetMatchData(MatchKey)['score_breakdown'][red or blue] [the other stuff]
['autoChargeStationPoints']
['autoBridgeState']
['autoChargeStationRobot1']
['autoChargeStationRobot2']
['autoChargeStationRobot3']
['totalChargeStationPoints']
['endGameChargeStationPoints']
['endGameBridgeState']
['endGameChargeStationRobot1']
['endGameChargeStationRobot2']
['endGameChargeStationRobot3']

[teleopGamePiecePoints]
have method the reads ['teleopCommunity']['B'], ['teleopCommunity']['M'], ['teleopCommunity']['T']


#Code not transferred over starting line 412 of app script, if you want to work on it, please start converting methods over there first

#prettyPrint(TBA_TeamEventQualRank(TBA_EventTeamsFormatted(curEvent)[1],curEvent))



#fills entire sheet
def fill_matchdata():   
    matches = TBA_EventMatchKeys(curEvent) 
    now = datetime.now().time()
    current_time = timedelta(hours=float(now.hour),minutes=float(now.minute),seconds=float(now.second))

    for match in matches:
        cur_match_data= TBA_GetCurMatch(match)
        #prettyPrint( TBA_MatchWinner(match))
        #we have the mathc data now, we fill in each match with the data, code not implemented yet
        
    now = datetime.now().time()
    finished_time = timedelta(hours=float(now.hour),minutes=float(now.minute),seconds=float(now.second))
    print (finished_time - current_time)


#fill_matchdata()

#print (json.dumps(req, indent=2))
# red_score = req['score_breakdown']['red']['autoPoints']
# print (red_score)


#print (TBANewCustom(req,'score_breakdown','red','autoPoints'))
