
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

def TBA_TeamNickname(team):
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


def OPR(team):
    return TBA_EventOPRs(curEvent)['oprs']['frc'+team]
def DPR(team):
    return TBA_EventOPRs(curEvent)['dprs']['frc'+team]
def CCWM(team):
    return TBA_EventOPRs(curEvent)['ccwms']['frc'+team]

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

# def GetMatchData(MatchKey):
#     return TBA_EventMatchKeys(curEvent)[MatchKey]



    
def GetBlueRP(match):
    return match['score_breakdown']['blue']['rp']

def GetRedRP(match):
    return match['score_breakdown']['red']['rp']

def GetBlueScore(match):
    return match['score_breakdown']['blue']['totalPoints']

def GetRedScore(match):
    return match['score_breakdown']['red']['totalPoints']

def GetBlueTeams(match): 
    return match['alliances']['blue']['team_keys']

def GetRedTeams(match): 
    return match['alliances']['red']['team_keys']

def GetBlueAutoPoints(match):
    return match['score_breakdown']['blue']['autoPoints']

def GetRedAutoPoints(match):
    return match['score_breakdown']['red']['autoPoints']

def GetBlueAutoChargeStationPoints(match):
    return match['score_breakdown']['blue']['autoChargeStationPoints']

def GetBlueAutoBridgeState(match):
    return match['score_breakdown']['blue']['autoBridgeState']

def GetBlueAutoChargeStationRobot1(match):
    return match['score_breakdown']['blue']['autoChargeStationRobot1']

def GetBlueAutoChargeStationRobot2(match):
    return match['score_breakdown']['blue']['autoChargeStationRobot2']

def GetBlueAutoChargeStationRobot3(match):
    return match['score_breakdown']['blue']['autoChargeStationRobot3']

def GetBlueTotalChargeStationPoints(match):
    return match['score_breakdown']['blue']['totalChargeStationPoints']

def GetBlueEndGameChargeStationPoints(match):
    return match['score_breakdown']['blue']['endGameChargeStationPoints']

def GetBlueEndGameBridgeState(match):
    return match['score_breakdown']['blue']['endGameBridgeState']

def GetBlueEndGameChargeStationRobot1(match):
    return match['score_breakdown']['blue']['endGameChargeStationRobot1']

def GetBlueEndGameChargeStationRobot2(match):
    return match['score_breakdown']['blue']['endGameChargeStationRobot2']

def GetBlueEndGameChargeStationRobot3(match):
    return match['score_breakdown']['blue']['endGameChargeStationRobot3']

def GetRedAutoChargeStationPoints(match):
    return match['score_breakdown']['red']['autoChargeStationPoints']

def GetRedAutoBridgeState(match):
    return match['score_breakdown']['red']['autoBridgeState']

def GetRedAutoChargeStationRobot1(match):
    return match['score_breakdown']['red']['autoChargeStationRobot1']

def GetRedAutoChargeStationRobot2(match):
    return match['score_breakdown']['red']['autoChargeStationRobot2']

def GetRedAutoChargeStationRobot3(match):
    return match['score_breakdown']['red']['autoChargeStationRobot3']

def GetRedTotalChargeStationPoints(match):
    return match['score_breakdown']['red']['totalChargeStationPoints']

def GetRedEndGameChargeStationPoints(match):
    return match['score_breakdown']['red']['endGameChargeStationPoints']

def GetRedEndGameBridgeState(match):
    return match['score_breakdown']['red']['endGameBridgeState']

def GetRedEndGameChargeStationRobot1(match):
    return match['score_breakdown']['red']['endGameChargeStationRobot1']

def GetRedEndGameChargeStationRobot2(match):
    return match['score_breakdown']['red']['endGameChargeStationRobot2']

def GetRedEndGameChargeStationRobot3(match):
    return match['score_breakdown']['red']['endGameChargeStationRobot3']

def GetBlueTeleopGamePiecePoints(match):
    return match['score_breakdown']['blue']['teleopGamePiecePoints']

def GetRedTeleopGamePiecePoints(match):
    return match['score_breakdown']['red']['teleopGamePiecePoints']

def GetBlueTeleopGamePieceB(match):
    return match['score_breakdown']['blue']['teleopCommunity']['B']

def GetRedTeleopGamePieceB(match):
    return match['score_breakdown']['red']['teleopCommunity']['B']

def GetBlueTeleopGamePieceM(match):
    return match['score_breakdown']['blue']['teleopCommunity']['M']

def GetRedTeleopGamePieceM(match):
    return match['score_breakdown']['red']['teleopCommunity']['M']

def GetBlueTeleopGamePieceT(match):
    return match['score_breakdown']['blue']['teleopCommunity']['T']

def GetRedTeleopGamePieceT(match):
    return match['score_breakdown']['red']['teleopCommunity']['T']

#we need to use the bottom middle and top rows to find the specific amount of cube points scord, and telopgamepeicepoint-cube = cone



# BELOW is the "tester" where we print out all the match data for each match in a given event. We also print out the time 
# it takes for this method to run. 
# We have NOT written anything to actually write the prints to the spreadsheet, that is one of our next goals



#fills entire sheet
def fill_matchdata():   
    matches = TBA_EventMatchKeys(curEvent) 
    now = datetime.now().time()
    current_time = timedelta(hours=float(now.hour),minutes=float(now.minute),seconds=float(now.second))

    for match in matches:
        cur_match_data= TBA_GetCurMatch(match)
        
        print ("====== Printing match data for " + str(match) + " ======")
        
        prettyPrint(GetBlueRP(cur_match_data))
        prettyPrint(GetRedRP(cur_match_data))
        prettyPrint(GetBlueScore(cur_match_data))
        prettyPrint(GetRedScore(cur_match_data))
        
        print()
        
        prettyPrint(GetBlueTeams(cur_match_data))
        prettyPrint(GetRedTeams(cur_match_data))
        
        print()
        
        prettyPrint(GetBlueAutoPoints(cur_match_data))
        prettyPrint(GetRedAutoPoints(cur_match_data))
        prettyPrint(GetBlueAutoChargeStationPoints(cur_match_data))
        prettyPrint(GetBlueAutoBridgeState(cur_match_data))
        prettyPrint(GetBlueAutoChargeStationRobot1(cur_match_data))
        prettyPrint(GetBlueAutoChargeStationRobot2(cur_match_data))
        prettyPrint(GetBlueAutoChargeStationRobot3(cur_match_data))
        prettyPrint(GetBlueTotalChargeStationPoints(cur_match_data))
        prettyPrint(GetBlueEndGameChargeStationPoints(cur_match_data))
        prettyPrint(GetBlueEndGameBridgeState(cur_match_data))
        prettyPrint(GetBlueEndGameChargeStationRobot1(cur_match_data))
        prettyPrint(GetBlueEndGameChargeStationRobot2(cur_match_data))
        prettyPrint(GetBlueEndGameChargeStationRobot3(cur_match_data))
        
        print()
        
        prettyPrint(GetRedAutoChargeStationPoints(cur_match_data))
        prettyPrint(GetRedAutoBridgeState(cur_match_data))
        prettyPrint(GetRedAutoChargeStationRobot1(cur_match_data))
        prettyPrint(GetRedAutoChargeStationRobot2(cur_match_data))
        prettyPrint(GetRedAutoChargeStationRobot3(cur_match_data))
        prettyPrint(GetRedTotalChargeStationPoints(cur_match_data))
        prettyPrint(GetRedEndGameChargeStationPoints(cur_match_data))
        prettyPrint(GetRedEndGameBridgeState(cur_match_data))
        prettyPrint(GetRedEndGameChargeStationRobot1(cur_match_data))
        prettyPrint(GetRedEndGameChargeStationRobot2(cur_match_data))
        prettyPrint(GetRedEndGameChargeStationRobot3(cur_match_data))
        
        print()
        
        prettyPrint(GetBlueTeleopGamePiecePoints(cur_match_data))
        prettyPrint(GetRedTeleopGamePiecePoints(cur_match_data))
        prettyPrint(GetBlueTeleopGamePieceB(cur_match_data))
        prettyPrint(GetRedTeleopGamePieceB(cur_match_data))
        prettyPrint(GetBlueTeleopGamePieceM(cur_match_data))
        prettyPrint(GetRedTeleopGamePieceM(cur_match_data))
        prettyPrint(GetBlueTeleopGamePieceT(cur_match_data))
        prettyPrint(GetRedTeleopGamePieceT(cur_match_data))
        
        print()
        print()
        print()
        
        #prettyPrint( TBA_MatchWinner(match))
        #we have the mathc data now, we fill in each match with the data, code not implemented yet
        
    now = datetime.now().time()
    finished_time = timedelta(hours=float(now.hour),minutes=float(now.minute),seconds=float(now.second))
    print (finished_time - current_time)


#fill_matchdata()

