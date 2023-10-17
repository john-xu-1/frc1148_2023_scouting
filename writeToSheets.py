import pygsheets
import pandas as pd
import TBA_Functions as tb
#authorization
curEvent = "2023cala"

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

# cone points per match

# data['OPR-cone

# cube points per match

# OPR-cube

DPR = tb.TBA_EventDPR(curEvent)

CCWM = tb.TBA_EventCCWM(curEvent)

winRates = []
for i in range (len(Teams)):
   winRates.append(tb.TBA_WinRate(Teams[i],curEvent))

data = pd.DataFrame({"Teams":Teams,"OPR":OPR, "DPR":DPR, "CCWM":CCWM, "Win Rate %": winRates})
print ("start writing power rating data")
sh = gc.open('Scouting Spreadsheet')
wks = sh[1]
wks.set_dataframe(data,(1,1))

print("starting tba data (+parking)")

def extract_data(data_type, Match):
    data_list = []
    for i in range(len(Match)):
        data_list.append(data_type(Match[i]))
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

BlueRP = extract_data(tb.GetBlueRP, Match)

BlueScore= extract_data(tb.GetBlueScore, Match)

BlueAlliance= extract_data(tb.GetBlueTeams, Match)

RedRP= extract_data(tb.GetRedRP, Match)

RedScore = extract_data(tb.GetRedScore, Match)
    
RedAlliance= extract_data(tb.GetRedTeams, Match)
    
BlueTotalAutopts= extract_data(tb.GetBlueAutoPoints, Match)
    
BluetotalChargeStationPoints= extract_data(tb.GetBlueTotalChargeStationPoints, Match)
    
BlueAutoStationpts= extract_data(tb.GetBlueAutoChargeStationPoints, Match)
    
BlueAutoStationlvl= extract_data(tb.GetBlueAutoBridgeState, Match)
    
BlueAutoPark1= extract_data(tb.GetBlueAutoChargeStationRobot1, Match)
  
BlueAutoPark2= extract_data(tb.GetBlueAutoChargeStationRobot2, Match)
    
BlueAutoPark3= extract_data(tb.GetBlueAutoChargeStationRobot3, Match)

BlueendGameChargeStationPoints= extract_data(tb.GetBlueEndGameChargeStationPoints, Match)
  
BlueendGameBridgeState= extract_data(tb.GetBlueEndGameBridgeState, Match)
  
BlueEndgamePark1= extract_data(tb.GetBlueEndGameChargeStationRobot1, Match)
    
BlueEndgamePark2= extract_data(tb.GetBlueEndGameChargeStationRobot2, Match)
    
BlueEndgamePark3= extract_data(tb.GetBlueEndGameChargeStationRobot3, Match)
  
RedTotalAutopts= extract_data(tb.GetRedAutoPoints, Match)
    
RedtotalChargeStationPoints= extract_data(tb.GetRedTotalChargeStationPoints, Match)
    
RedAutoStationpts= extract_data(tb.GetRedAutoChargeStationPoints, Match)
    
RedAutoStationlvl= extract_data(tb.GetRedAutoBridgeState, Match)
    
RedAutoPark1= extract_data(tb.GetRedAutoChargeStationRobot1, Match)

RedAutoPark2= extract_data(tb.GetRedAutoChargeStationRobot2, Match)
    
RedAutoPark3= extract_data(tb.GetRedAutoChargeStationRobot3, Match)

RedendGameChargeStationPoints= extract_data(tb.GetRedEndGameChargeStationPoints, Match)

RedendGameBridgeState= extract_data(tb.GetRedEndGameBridgeState, Match)
 
RedEndgamePark1= extract_data(tb.GetRedEndGameChargeStationRobot1, Match)
    
RedEndgamePark2= extract_data(tb.GetRedEndGameChargeStationRobot2, Match)
   
RedEndgamePark3= extract_data(tb.GetRedEndGameChargeStationRobot3, Match)
   
Winner = extract_data(tb.TBA_MatchWinner, match)
    
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
    "Blue totalChargeStationPoints": BluetotalChargeStationPoints,
    "Blue Auto Station pts": BlueAutoStationpts,
    "Blue Auto Station lvl": BlueAutoStationlvl,
    "Blue Auto Park 1": BlueAutoPark1,
    "Blue Auto Park 2": BlueAutoPark2,
    "Blue Auto Park 3": BlueAutoPark3,
    "Blue endGameChargeStationPoints": BlueendGameChargeStationPoints,
    "Blue endGameBridgeState": BlueendGameBridgeState,
    "Blue Endgame Park 1": BlueEndgamePark1,
    "Blue Endgame Park 2": BlueEndgamePark2,
    "Blue Endgame Park 3": BlueEndgamePark3,
    "Red Total Auto pts": RedTotalAutopts,
    "Red totalChargeStationPoints": RedtotalChargeStationPoints,
    "Red Auto Station pts": RedAutoStationpts,
    "Red Auto Station lvl": RedAutoStationlvl,
    "Red Auto Park 1": RedAutoPark1,
    "Red Auto Park 2": RedAutoPark2,
    "Red Auto Park 3": RedAutoPark3,
    "Red endGameChargeStationPoints": RedendGameChargeStationPoints,
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

print("all done")