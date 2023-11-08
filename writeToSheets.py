import pygsheets
import pandas as pd
import TBA_Functions as tb
import CalculateOPR as cop
import numpy as np
#authorization
curEvent = "2023catt"

gc = pygsheets.authorize(service_file='credentials.json')

# # Create empty dataframe
# df = pd.DataFrame()

# # Create a column
# df['name'] = ['John', 'Mathew', 'Sarah']

# #open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
# sh = gc.open('Scouting Spreadsheet')

# #select the first sheet 
# wks = sh[0]

# #update the first sheet with df, starting at cell B2. 
# wks.set_dataframe(df,(1,1))

print("starting power ratings")

Teams = tb.TBA_EventTeamsFormatted(curEvent)

OPR = tb.TBA_EventOPR(curEvent)

coneNCube = cop.coneNcubeOPR(event=curEvent)

matchesPlayed = []



for team in Teams:
    status = tb.TBA_TeamEventStatus(team,curEvent)["qual"]
    if (status  is not None):
        matchesPlayed.append(tb.TBA_MatchesPlayed(team, curEvent))
    else: matchesPlayed.append("None")

DPR = tb.TBA_EventDPR(curEvent)

CCWM = tb.TBA_EventCCWM(curEvent)

print (len(Teams))
print (len(OPR[:36]))


winRates = []
for i in range (len(Teams)):
    status = tb.TBA_TeamEventStatus(team,curEvent)["qual"]
    if (status is not None):
        winRates.append(tb.TBA_WinRate(Teams[i],curEvent))
    else: winRates.append("None")

print (len(coneNCube['coneOPR']))
print (len( winRates))
print (len(matchesPlayed))


data = pd.DataFrame({"Teams":Teams,"OPR":OPR[:36], "DPR":DPR[:36], "CCWM":CCWM[:36], "Win Rate %": winRates, "Cone OPR": coneNCube['coneOPR'], "Cube OPR": coneNCube['cubeOPR'], "Matches Played": matchesPlayed})
print ("start writing power rating data")
sh = gc.open('Scouting Spreadsheet')
wks = sh[1]
wks.set_dataframe(data,(1,1))

print("starting tba data (+parking)")



def extract_data(data_type, Match):
    data_list = []
    
    
    
    for i in range(len(Match)):
        #cur_match_data= tb.TBA_GetCurMatch(match[i])
        data_list.append(data_type(Match[i]))
        
        # if type(cur_match_data['score_breakdown']) is not type(None):
        #     print (cur_match_data)
            
        # else: data_list.append ("none")
    print ("========================= finished once ==============================")
    return data_list

def EventMatchKeys(x):
    match_keys = tb.TBA_AddressFetcher("event/" + x + "/matches/keys")
    matches = []

    for match_key in match_keys:
        match_data = tb.TBA_GetCurMatch(match_key)
        matches.append(match_data)

    return matches

Match = EventMatchKeys(curEvent)
match = tb.TBA_EventMatchKeys(curEvent)




#BlueRP, BlueScore, BlueAlliance, RedAlliance, RedRP, RedScore, BlueTotalAutopts, BluetotalChargeStationPoints, BlueAutoStationpts, BlueAutoStationlvl, BlueAutoPark1, BlueAutoPark2, BlueAutoPark3, BlueEndgamePark1, BlueEndgamePark2, BlueEndgamePark3, Winner = []
#RedTotalAutopts, RedtotalChargeStationPoints, RedAutoStationpts, RedAutoStationlvl, RedeAutoPark1, RedAutoPark2, RedAutoPark3, RedEndgamePark1, RedEndgamePark2, RedEndgamePark3 = []  




BlueRP = extract_data(tb.GetBlueRP, Match)

BlueScore= extract_data(tb.GetBlueScore, Match)

BlueAlliance= extract_data(tb.GetBlueTeams, Match)

RedAlliance= extract_data(tb.GetRedTeams, Match)

RedRP= extract_data(tb.GetRedRP, Match)


RedScore = extract_data(tb.GetRedScore, Match)
    

    
BlueTotalAutopts= extract_data(tb.GetBlueAutoPoints, Match)
    
BluetotalChargeStationPoints= [] #extract_data(tb.GetBlueTotalChargeStationPoints, Match)
    
BlueAutoStationpts= [] #extract_data(tb.GetBlueAutoChargeStationPoints, Match)
    
BlueAutoStationlvl= [] #extract_data(tb.GetBlueAutoBridgeState, Match)
    
BlueAutoPark1= extract_data(tb.GetBlueAutoChargeStationRobot1, Match)

BlueAutoPark2= extract_data(tb.GetBlueAutoChargeStationRobot2, Match)
    
BlueAutoPark3= extract_data(tb.GetBlueAutoChargeStationRobot3, Match)

BlueendGameChargeStationPoints= [] #extract_data(tb.GetBlueEndGameChargeStationPoints, Match)

BlueendGameBridgeState= extract_data(tb.GetBlueEndGameBridgeState, Match)

BlueEndgamePark1= extract_data(tb.GetBlueEndGameChargeStationRobot1, Match)
    
BlueEndgamePark2= extract_data(tb.GetBlueEndGameChargeStationRobot2, Match)
    
BlueEndgamePark3= extract_data(tb.GetBlueEndGameChargeStationRobot3, Match)

RedTotalAutopts= extract_data(tb.GetRedAutoPoints, Match)
    
RedtotalChargeStationPoints= [] #extract_data(tb.GetRedTotalChargeStationPoints, Match)
    
RedAutoStationpts= [] #extract_data(tb.GetRedAutoChargeStationPoints, Match)
    
RedAutoStationlvl= [] #extract_data(tb.GetRedAutoBridgeState, Match)
    
RedAutoPark1= extract_data(tb.GetRedAutoChargeStationRobot1, Match)

RedAutoPark2= extract_data(tb.GetRedAutoChargeStationRobot2, Match)
    
RedAutoPark3= extract_data(tb.GetRedAutoChargeStationRobot3, Match)

RedendGameChargeStationPoints= [] #extract_data(tb.GetRedEndGameChargeStationPoints, Match)

RedendGameBridgeState= extract_data(tb.GetRedEndGameBridgeState, Match)

RedEndgamePark1= extract_data(tb.GetRedEndGameChargeStationRobot1, Match)
    
RedEndgamePark2= extract_data(tb.GetRedEndGameChargeStationRobot2, Match)

RedEndgamePark3= extract_data(tb.GetRedEndGameChargeStationRobot3, Match)

Winner = extract_data(tb.TBA_MatchWinner, match)

sizes = []

sizes.append(len(BlueRP))
sizes.append(len(BlueAlliance))
sizes.append(len(BlueScore))
sizes.append(len(RedRP))
sizes.append(len(RedScore))
sizes.append(len(RedAlliance))
sizes.append(len(Winner))

sizes.append(len(BlueTotalAutopts))
#sizes.append(len(BluetotalChargeStationPoints))
#sizes.append(len(BlueAutoStationpts))
#sizes.append(len(BlueAutoStationlvl))
sizes.append(len(BlueAutoPark1))
sizes.append(len(BlueAutoPark2))
sizes.append(len(BlueAutoPark3))
#sizes.append(len(BlueendGameChargeStationPoints))
sizes.append(len(BlueendGameBridgeState))
sizes.append(len(BlueEndgamePark1))
sizes.append(len(BlueEndgamePark2))
sizes.append(len(BlueEndgamePark3))

sizes.append(len(RedTotalAutopts))
#sizes.append(len(RedtotalChargeStationPoints))
#sizes.append(len(RedAutoStationpts))
#sizes.append(len(RedAutoStationlvl))
sizes.append(len(RedAutoPark1))
sizes.append(len(RedAutoPark2))
sizes.append(len(RedAutoPark3))
#sizes.append(len(RedendGameChargeStationPoints))
sizes.append(len(RedendGameBridgeState))
sizes.append(len(RedEndgamePark1))
sizes.append(len(RedEndgamePark2))
sizes.append(len(RedEndgamePark3))



# BlueRP = BlueRP[:min]
# BlueAlliance = BlueAlliance[:min]
# BlueScore = BlueScore[:min]
# RedRP = RedRP[:min]
# RedScore = RedScore[:min]
# RedAlliance = RedAlliance[:min]
# Winner = Winner[:min]

# BlueTotalAutopts = BlueTotalAutopts[:min]
# #sizes.append(len(BluetotalChargeStationPoints))
# #sizes.append(len(BlueAutoStationpts))
# #sizes.append(len(BlueAutoStationlvl))
# BlueAutoPark1 = BlueAutoPark1[:min]
# BlueAutoPark2 = BlueAutoPark2[:min]
# BlueAutoPark3 = BlueAutoPark3[:min]
# BlueendGameChargeStationPoints = BlueendGameChargeStationPoints[:min]
# BlueendGameBridgeState = BlueendGameBridgeState[:min]
# BlueEndgamePark1 = BlueEndgamePark1[:min]
# BlueEndgamePark2 = BlueEndgamePark2[:min]
# BlueEndgamePark3 = BlueEndgamePark3[:min]

# RedTotalAutopts = RedTotalAutopts[:min]
# #sizes.append(len(BluetotalChargeStationPoints))
# #sizes.append(len(BlueAutoStationpts))
# #sizes.append(len(BlueAutoStationlvl))
# RedAutoPark1 = RedAutoPark1[:min]
# RedAutoPark2 = RedAutoPark2[:min]
# RedAutoPark3 = RedAutoPark3[:min]
# RedendGameChargeStationPoints = RedendGameChargeStationPoints[:min]
# RedendGameBridgeState = RedendGameBridgeState[:min]
# RedEndgamePark1 = RedEndgamePark1[:min]
# RedEndgamePark2 = RedEndgamePark2[:min]
# RedEndgamePark3 = RedEndgamePark3[:min]

# RedtotalChargeStationPoints= [None] * min #extract_data(tb.GetRedTotalChargeStationPoints, Match)
    
# RedAutoStationpts= [None] * min #extract_data(tb.GetRedAutoChargeStationPoints, Match)
    
# RedAutoStationlvl= [None] * min #extract_data(tb.GetRedAutoBridgeState, Match)
# RedendGameChargeStationPoints = [None] * min



# BluetotalChargeStationPoints= [None] * min #extract_data(tb.GetRedTotalChargeStationPoints, Match)
    
# BlueAutoStationpts= [None] * min #extract_data(tb.GetRedAutoChargeStationPoints, Match)
    
# BlueAutoStationlvl= [None] * min #extract_data(tb.GetRedAutoBridgeState, Match)
# BlueendGameChargeStationPoints = [None] * min
 
    
data2 = pd.DataFrame({
    "Matches":match,
    "Blue RP": BlueRP,
    "Blue Score": BlueScore,
    "Blue Alliance": BlueAlliance,
    "Red RP": RedRP,
    "Red Score": RedScore,
    "Red Alliance": RedAlliance,
    "Winner": Winner,
    "Blue Total Auto pts": BlueTotalAutopts,
    # "Blue totalChargeStationPoints": BluetotalChargeStationPoints,
    # "Blue Auto Station pts": BlueAutoStationpts,
    # "Blue Auto Station lvl": BlueAutoStationlvl,
    "Blue Auto Park 1": BlueAutoPark1,
    "Blue Auto Park 2": BlueAutoPark2,
    "Blue Auto Park 3": BlueAutoPark3,
    # "Blue endGameChargeStationPoints": BlueendGameChargeStationPoints,
    "Blue endGameBridgeState": BlueendGameBridgeState,
    "Blue Endgame Park 1": BlueEndgamePark1,
    "Blue Endgame Park 2": BlueEndgamePark2,
    "Blue Endgame Park 3": BlueEndgamePark3,
    "Red Total Auto pts": RedTotalAutopts,
    # "Red totalChargeStationPoints": RedtotalChargeStationPoints,
    # "Red Auto Station pts": RedAutoStationpts,
    # "Red Auto Station lvl": RedAutoStationlvl,
    "Red Auto Park 1": RedAutoPark1,
    "Red Auto Park 2": RedAutoPark2,
    "Red Auto Park 3": RedAutoPark3,
    # "Red endGameChargeStationPoints": RedendGameChargeStationPoints,
    "Red endGameBridgeState": RedendGameBridgeState,
    "Red Endgame Park 1": RedEndgamePark1,
    "Red Endgame Park 2": RedEndgamePark2,
    "Red Endgame Park 3": RedEndgamePark3
}
)
print ("start writing data for tba data")
sh = gc.open('Scouting Spreadsheet')
wks = sh[2]
wks.set_dataframe(data2,(1,1))


B = pd.DataFrame({"BlueAlliance":BlueAlliance})
R = pd.DataFrame({"RedAlliance":RedAlliance})
print ("start writing data for scouting")
sh = gc.open('Scouting Spreadsheet')
wks = sh[3]
wks.set_dataframe(B,(1,5))
wks.set_dataframe(R,(1,9))


print("all done")