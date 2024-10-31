
import requests
import json
from datetime import datetime, timedelta

curEvent = "2024catt"
# 2024caph

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

def TBA_MatchesPlayed(team,event):
    return TBA_TeamEventStatus(team,event)["qual"]["ranking"]["matches_played"]
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
    if TBA_AddressFetcher("event/"+event+"/oprs") is not None:
        return TBA_AddressFetcher("event/"+event+"/oprs")

def TBA_EventOPR(event):
    if (TBA_AddressFetcher("event/" + event + "/oprs") is not None):
        OPRs = TBA_AddressFetcher("event/" + event + "/oprs")['oprs']
        OPR_values = list(OPRs.values())
        return OPR_values

def TBA_EventDPR(event):
    OPRs = TBA_AddressFetcher("event/" + event + "/oprs")['dprs']
    OPR_values = list(OPRs.values())
    return OPR_values

def TBA_EventCCWM(event):
    OPRs = TBA_AddressFetcher("event/" + event + "/oprs")['ccwms']
    OPR_values = list(OPRs.values())
    return OPR_values

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
    if match['score_breakdown']is not None:
        return match["winning_alliance"]

def GetCoopertitionBonusAchieved(match):
    if match.get('score_breakdown') and match['score_breakdown'].get('blue'):
        if match['score_breakdown']['blue'].get('coopertitionBonusAchieved') is not None:
            return match['score_breakdown']['blue']['coopertitionBonusAchieved']
    return None
# def GetMatchData(MatchKey):
#     return TBA_EventMatchKeys(curEvent)[MatchKey]

    
def GetBlueRP(match):
    if match['score_breakdown']is not None:
        return match['score_breakdown']['blue']['rp']
 
def GetBlueTele(match):
    if match['score_breakdown']is not None:
        return match['score_breakdown']['blue']['teleopTotalNotePoints']
    
def GetRedTele(match):
    if match['score_breakdown']is not None:
        return match['score_breakdown']['red']['teleopTotalNotePoints']

def GetRedRP(match):
    if match['score_breakdown'] is not None:
        return match['score_breakdown']['red']['rp']

def GetBlueScore(match):
    if match['score_breakdown'] is not None:
        return match['score_breakdown']['blue']['totalPoints']

def GetRedScore(match):
    if match['score_breakdown'] is not None:
        return match['score_breakdown']['red']['totalPoints']

def GetBlueTeams(match):
    if match['alliances']['blue'] is not None: 
        return match['alliances']['blue']['team_keys']

def GetRedTeams(match): 
    if match['alliances']['red'] is not None: 
        return match['alliances']['red']['team_keys']

def GetBlueAutoPoints(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['blue']['autoPoints']

def GetRedAutoPoints(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['red']['autoPoints']
   
 
def GetBlueAutoAmpPoints(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['blue']['autoAmpNotePoints']
    
def GetBlueTeleAmpPoints(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['blue']['teleopAmpNotePoints']
    
def GetBlueAutoSpeakerPoints(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['blue']['autoSpeakerNotePoints']

def GetBlueSpeakerPointsRegular(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['blue']['teleopSpeakerNotePoints']
    
def GetBlueTeleSpeakerPointsAmped(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['blue']['teleopSpeakerNoteAmplifiedPoints']

def GetBlueCenterTrapPoints(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['blue']['trapCenterStage']
    
def GetBlueLeftTrapPoints(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['blue']['trapStageLeft']
    
def GetBlueRightTrapPoints(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['blue']['trapStageRight']

def GetBlueParkStatus1(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['blue']['endGameRobot1']
    
def GetBlueParkStatus2(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['blue']['endGameRobot2']
    
def GetBlueParkStatus3(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['blue']['endGameRobot3']

def GetBlueCenterMicStatus(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['blue']['micCenterStage']
    
def GetBlueLeftMicStatus(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['blue']['micStageLeft']
    
def GetBlueRightMicStatus(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['blue']['micStageRight']
    
def GetBlueHarmonyPoints (match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['blue']['endGameHarmonyPoints']
    
def GetBlueCoopTry (match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['blue']['coopNotePlayed']

def GetRedAutoAmpPoints(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['red']['autoAmpNotePoints']
    
def GetRedTeleAmpPoints(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['red']['teleopAmpNotePoints']
    
def GetRedAutoSpeakerPoints(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['red']['autoSpeakerNotePoints']

def GetRedSpeakerPointsRegular(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['red']['teleopSpeakerNotePoints']
    
def GetRedTeleSpeakerPointsAmped(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['red']['teleopSpeakerNoteAmplifiedPoints']

def GetRedCenterTrapPoints(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['red']['trapCenterStage']
    
def GetRedLeftTrapPoints(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['red']['trapStageLeft']
    
def GetRedRightTrapPoints(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['red']['trapStageRight']

def GetRedParkStatus1(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['red']['endGameRobot1']
    
def GetRedParkStatus2(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['red']['endGameRobot2']
    
def GetRedParkStatus3(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['red']['endGameRobot3']

def GetRedCenterMicStatus(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['red']['micCenterStage']
    
def GetRedLeftMicStatus(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['red']['micStageLeft']
    
def GetRedRightMicStatus(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['red']['micStageRight']
    
def GetRedHarmonyPoints(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['red']['endGameHarmonyPoints']
    
def GetRedCoopTry(match):
    if match.get('score_breakdown') and match['score_breakdown'].get('red'):
        return match['score_breakdown']['red'].get('coopNotePlayed')
    return None

def GetBlueAmpCount(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['blue']['teleopAmpNoteCount']

def GetBlueSpeakerCount(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['blue']['teleopSpeakerNoteAmplifiedCount']

def GetBlueSpeakerAmpedCount(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['blue']['teleopSpeakerNoteCount']

def GetRedAmpCount(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['red']['teleopAmpNoteCount']

def GetRedSpeakerCount(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['red']['teleopSpeakerNoteAmplifiedCount']

def GetRedSpeakerAmpedCount(match):
    if match['score_breakdown'] is not None: 
        return match['score_breakdown']['red']['teleopSpeakerNoteCount']

# def GetBlueAutoChargeStationPoints(match):
#     if match['score_breakdown'] is not None: 
#         return match['score_breakdown']['blue']['autoChargeStationPoints']

# def GetBlueAutoBridgeState(match):
#     if match['score_breakdown'] is not None: 
#         return match['score_breakdown']['blue']['autoBridgeState']

# def GetBlueAutoChargeStationRobot1(match):
#     if match['score_breakdown'] is not None: 
#         return match['score_breakdown']['blue']['autoChargeStationRobot1']
#     return None

# def GetBlueAutoChargeStationRobot2(match):
#     if match['score_breakdown'] is not None: 
#         return match['score_breakdown']['blue']['autoChargeStationRobot2']

# def GetBlueAutoChargeStationRobot3(match):
#     if match['score_breakdown'] is not None: 
#         return match['score_breakdown']['blue']['autoChargeStationRobot3']

# def GetBlueTotalChargeStationPoints(match):
#     if match['score_breakdown'] is not None:
#         print (match['score_breakdown']['blue'])
#         return match['score_breakdown']['blue']['totalChargeStationPoints']

# def GetBlueEndGameChargeStationPoints(match):
#     if match['score_breakdown'] is not None: 
#         return match['score_breakdown']['blue']['endGameChargeStationPoints']

# def GetBlueEndGameBridgeState(match):
#     if match['score_breakdown'] is not None: 
#         return match['score_breakdown']['blue']['endGameBridgeState']

# def GetBlueEndGameChargeStationRobot1(match):
#     if match['score_breakdown'] is not None: 
#         return match['score_breakdown']['blue']['endGameChargeStationRobot1']

# def GetBlueEndGameChargeStationRobot2(match):
#     if match['score_breakdown'] is not None: 
#         return match['score_breakdown']['blue']['endGameChargeStationRobot2']

# def GetBlueEndGameChargeStationRobot3(match):
#     if match['score_breakdown'] is not None: 
#         return match['score_breakdown']['blue']['endGameChargeStationRobot3']

# def GetRedAutoChargeStationPoints(match):
#     if match['score_breakdown'] is not None: 
#         return match['score_breakdown']['red']['autoChargeStationPoints']

# def GetRedAutoBridgeState(match):
#     if match['score_breakdown'] is not None: 
#         return match['score_breakdown']['red']['autoBridgeState']

# def GetRedAutoChargeStationRobot1(match):
#     if match['score_breakdown'] is not None:
#         return match['score_breakdown']['red']['autoChargeStationRobot1']

# def GetRedAutoChargeStationRobot2(match):
#     if match['score_breakdown'] is not None:
#         return match['score_breakdown']['red']['autoChargeStationRobot2']

# def GetRedAutoChargeStationRobot3(match):
#     if match['score_breakdown'] is not None:
#         return match['score_breakdown']['red']['autoChargeStationRobot3']

# def GetRedTotalChargeStationPoints(match):
#     if match['score_breakdown'] is not None: 
#         return match['score_breakdown']['red']['totalChargeStationPoints']

# def GetRedEndGameChargeStationPoints(match):
#     if match['score_breakdown'] is not None: 
#         return match['score_breakdown']['red']['endGameChargeStationPoints']

# def GetRedEndGameBridgeState(match):
#     if match['score_breakdown'] is not None:
#         return match['score_breakdown']['red']['endGameBridgeState']

# def GetRedEndGameChargeStationRobot1(match):
#     if match['score_breakdown'] is not None:
#         return match['score_breakdown']['red']['endGameChargeStationRobot1']

# def GetRedEndGameChargeStationRobot2(match):
#     if match['score_breakdown'] is not None:
#         return match['score_breakdown']['red']['endGameChargeStationRobot2']

# def GetRedEndGameChargeStationRobot3(match):
#     if match['score_breakdown'] is not None:
#         return match['score_breakdown']['red']['endGameChargeStationRobot3']

# def GetBlueTeleopGamePiecePoints(match):
#     if match['score_breakdown'] is not None: 
#         return match['score_breakdown']['blue']['teleopGamePiecePoints']

# def GetRedTeleopGamePiecePoints(match):
#     if match['score_breakdown'] is not None: 
#         return match['score_breakdown']['red']['teleopGamePiecePoints']

# def GetBlueTeleopGamePieceB(match):
#     if match['score_breakdown'] is not None: 
#         return match['score_breakdown']['blue']['teleopCommunity']['B']

# def GetRedTeleopGamePieceB(match):
#     if match['score_breakdown'] is not None: 
#         return match['score_breakdown']['red']['teleopCommunity']['B']

# def GetBlueTeleopGamePieceM(match):
#     if match['score_breakdown'] is not None: 
#         return match['score_breakdown']['blue']['teleopCommunity']['M']

# def GetRedTeleopGamePieceM(match):
#     if match['score_breakdown'] is not None: 
#         return match['score_breakdown']['red']['teleopCommunity']['M']

# def GetBlueTeleopGamePieceT(match):
#     if match['score_breakdown'] is not None: 
#         return match['score_breakdown']['blue']['teleopCommunity']['T']

# def GetRedTeleopGamePieceT(match):
#     if match['score_breakdown'] is not None: 
#         return match['score_breakdown']['red']['teleopCommunity']['T']

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
        
        # print ("====== Printing match data for " + str(match) + " ======")
        
        # prettyPrint(GetBlueRP(cur_match_data))
        # prettyPrint(GetRedRP(cur_match_data))
        # prettyPrint(GetBlueScore(cur_match_data))
        # prettyPrint(GetRedScore(cur_match_data))
        
        # print()
        
        # prettyPrint(GetBlueTeams(cur_match_data))
        # prettyPrint(GetRedTeams(cur_match_data))
        
        # print()
        
        # prettyPrint(GetBlueAutoPoints(cur_match_data))
        # prettyPrint(GetRedAutoPoints(cur_match_data))
        # prettyPrint(GetBlueAutoChargeStationPoints(cur_match_data))
        # prettyPrint(GetBlueAutoBridgeState(cur_match_data))
        # prettyPrint(GetBlueAutoChargeStationRobot1(cur_match_data))
        # prettyPrint(GetBlueAutoChargeStationRobot2(cur_match_data))
        # prettyPrint(GetBlueAutoChargeStationRobot3(cur_match_data))
        # prettyPrint(GetBlueTotalChargeStationPoints(cur_match_data))
        # prettyPrint(GetBlueEndGameChargeStationPoints(cur_match_data))
        # prettyPrint(GetBlueEndGameBridgeState(cur_match_data))
        # prettyPrint(GetBlueEndGameChargeStationRobot1(cur_match_data))
        # prettyPrint(GetBlueEndGameChargeStationRobot2(cur_match_data))
        # prettyPrint(GetBlueEndGameChargeStationRobot3(cur_match_data))
        
        # print()
        
        # prettyPrint(GetRedAutoChargeStationPoints(cur_match_data))
        # prettyPrint(GetRedAutoBridgeState(cur_match_data))
        # prettyPrint(GetRedAutoChargeStationRobot1(cur_match_data))
        # prettyPrint(GetRedAutoChargeStationRobot2(cur_match_data))
        # prettyPrint(GetRedAutoChargeStationRobot3(cur_match_data))
        # prettyPrint(GetRedTotalChargeStationPoints(cur_match_data))
        # prettyPrint(GetRedEndGameChargeStationPoints(cur_match_data))
        # prettyPrint(GetRedEndGameBridgeState(cur_match_data))
        # prettyPrint(GetRedEndGameChargeStationRobot1(cur_match_data))
        # prettyPrint(GetRedEndGameChargeStationRobot2(cur_match_data))
        # prettyPrint(GetRedEndGameChargeStationRobot3(cur_match_data))
        
        # print()
        
        # prettyPrint(GetBlueTeleopGamePiecePoints(cur_match_data))
        # prettyPrint(GetRedTeleopGamePiecePoints(cur_match_data))
        # prettyPrint(GetBlueTeleopGamePieceB(cur_match_data))
        # prettyPrint(GetRedTeleopGamePieceB(cur_match_data))
        # prettyPrint(GetBlueTeleopGamePieceM(cur_match_data))
        # prettyPrint(GetRedTeleopGamePieceM(cur_match_data))
        # prettyPrint(GetBlueTeleopGamePieceT(cur_match_data))
        # prettyPrint(GetRedTeleopGamePieceT(cur_match_data))
        
        # print()
        # print()
        # print()
        
        #prettyPrint( TBA_MatchWinner(match))
        
    now = datetime.now().time()
    finished_time = timedelta(hours=float(now.hour),minutes=float(now.minute),seconds=float(now.second))
    print (finished_time - current_time)


#fill_matchdata()

