import pygsheets
import pandas as pd
import TBA_Functions as tb
import CalculateOPR as cop
import numpy as np
import re
import re
import ast

def custom_sort(item_list):
    def custom_key(item):
        # Split the item into parts using '_' as the separator
        parts = item.split('_')

        # Define a dictionary to assign a sorting key to each part
        sorting_key = {
            'qm': 0,  # 'qm' comes first
            'sf': 1,  # 'sf' comes second
            'f': 2    # 'f' comes third
        }

        # Extract the type of the item (qm, sf, f) and the number part
        item_type = re.search(r'qm|sf|f', parts[1]).group(0)
        number_part = int(re.search(r'(\d+)$', parts[-1]).group(0))

        return sorting_key[item_type], number_part

    sorted_list = sorted(item_list, key=custom_key)

    return sorted_list

# def custom_sort_M(match_data_list):
#     def custom_key(match_data):
#         # Extract the match key
#         key = match_data.get('key', '')
#         return key

#     # Define a dictionary to assign a sorting key to each part
#     sorting_key = {
#         'qm': 0,  # 'qm' comes first
#         'sf': 1,  # 'sf' comes second
#         'f': 2    # 'f' comes third
#     }

#     sorted_list = sorted(match_data_list, key=lambda match_data: (sorting_key.get(match_data.get('comp_level'), 999), match_data.get('key')))
#     return sorted_list
def custom_sort_M(match_data_list):
    def custom_key(match_data):
        # Extract the match key
        key = match_data.get('key', '')
        return key

    # Define a dictionary to assign a sorting key to each part
    sorting_key = {
        'qm': 0,  # 'qm' comes first
        'sf': 1,  # 'sf' comes second
        'f': 2    # 'f' comes third
    }

    sorted_list = sorted(match_data_list, key=lambda match_data: (sorting_key.get(match_data.get('comp_level'), 999), match_data.get('match_number'), match_data.get('key')))
    return sorted_list


#authorization
curEvent = "2024week0"

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

speakerNAmps = cop.coneNcubeOPR(event=curEvent)

matchesPlayed = []

sh = gc.open('Scouting Spreadsheet')
wks = sh[5]

rows = wks.get_all_values()

avgAmpNum = {}
avgSpeakerNum = {}

for row in rows[1:]:
    name = row[0]
    if name != '':
        print (name)
        cutoff = name.index("c")
        name = name[cutoff+1:]
        if name in Teams:            
            if row[5] != '':
                if name not in avgAmpNum:
                    avgAmpNum[name] = 0
                avgAmpNum[name] += int(row[5])
                
            if row[2] != '':
                if name not in avgSpeakerNum:
                    avgSpeakerNum[name] = 0
                avgSpeakerNum[name] += int(row[2])

        
print (avgAmpNum)
print (avgSpeakerNum)


#values = result.get("values", [])




for team in Teams:
    if tb.TBA_TeamEventStatus(team,curEvent) is not None:
        status = tb.TBA_TeamEventStatus(team,curEvent)["qual"]
        if (status is not None):
            matchesPlayed.append(tb.TBA_MatchesPlayed(team, curEvent))
        else: matchesPlayed.append("None")
    if team not in avgAmpNum:
        avgAmpNum[team] = 0
    if team not in avgSpeakerNum:
        avgSpeakerNum[team] = 0


DPR = tb.TBA_EventDPR(curEvent)

CCWM = tb.TBA_EventCCWM(curEvent)

print (len(Teams))
print (len(OPR[:34]))


winRates = []
for i in range (len(Teams)):
    # status = tb.TBA_TeamEventStatus(team,curEvent)["qual"]
    # if (status is not None):
    #     winRates.append(tb.TBA_WinRate(Teams[i],curEvent))
    # else: winRates.append("None")
    winRates.append("None")

#print (len(coneNCube['coneOPR']))
print (len( winRates))
print (len(matchesPlayed))

#print (Teams)
sorted_avgAmpNum = sorted(avgAmpNum.items(), key=lambda x: Teams.index(x[0]) if x[0] in Teams else float('inf'))
sorted_avgSpeakerNum = sorted(avgSpeakerNum.items(), key=lambda x: Teams.index(x[0]) if x[0] in Teams else float('inf'))
print (len(sorted_avgAmpNum))
print (len (sorted_avgSpeakerNum))
print (len([item[1] for item in sorted_avgSpeakerNum] ))
print (len([item[1] for item in sorted_avgAmpNum] ))
print (sorted_avgAmpNum)

##changed the OPR[:36], "DPR":DPR[:36], "CCWM":CCWM[:36], to 47
data = pd.DataFrame({"Teams":Teams,"OPR":OPR[:34], "DPR":DPR[:34], "CCWM":CCWM[:34], "Win Rate %": winRates, "Amp OPR": speakerNAmps["ampOPR"], "Speaker OPR": speakerNAmps["speakerOPR"], "Matches Played": matchesPlayed, "Amps per Game": speakerNAmps["Amps"], "Speaker per Game": speakerNAmps["Speakers"], "Team Total Speaker": [item[1] for item in sorted_avgSpeakerNum], "Team Total Amp": [item[1] for item in sorted_avgAmpNum]})
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

Match = EventMatchKeys(curEvent)## Match info
match = tb.TBA_EventMatchKeys(curEvent)## Match keys


# Sort the list by category (qm, sf, f) and then by the number within each category
match = custom_sort(match)
Match = custom_sort_M(Match)
print (Match)


#BlueRP, BlueScore, BlueAlliance, RedAlliance, RedRP, RedScore, BlueTotalAutopts, BluetotalChargeStationPoints, BlueAutoStationpts, BlueAutoStationlvl, BlueAutoPark1, BlueAutoPark2, BlueAutoPark3, BlueEndgamePark1, BlueEndgamePark2, BlueEndgamePark3, Winner = []
#RedTotalAutopts, RedtotalChargeStationPoints, RedAutoStationpts, RedAutoStationlvl, RedeAutoPark1, RedAutoPark2, RedAutoPark3, RedEndgamePark1, RedEndgamePark2, RedEndgamePark3 = []  

CoopertitionBonusAchieved = extract_data(tb.GetCoopertitionBonusAchieved,Match)

BlueRP = extract_data(tb.GetBlueRP, Match)

BlueScore= extract_data(tb.GetBlueScore, Match)

BlueAlliance= extract_data(tb.GetBlueTeams, Match)

RedAlliance= extract_data(tb.GetRedTeams, Match)

RedRP= extract_data(tb.GetRedRP, Match)

RedScore = extract_data(tb.GetRedScore, Match)

Winner = extract_data(tb.TBA_MatchWinner, match)

RedAutoPoints = extract_data(tb.GetRedAutoPoints, Match)
BlueAutoPoints = extract_data(tb.GetBlueAutoPoints, Match)
RedRP = extract_data(tb.GetRedRP, Match)
BlueRP = extract_data(tb.GetBlueRP, Match)
RedScore = extract_data(tb.GetRedScore, Match)
BlueScore = extract_data(tb.GetBlueScore, Match)
RedTeams = extract_data(tb.GetRedTeams, Match)
BlueTeams = extract_data(tb.GetBlueTeams, Match)
RedAutoAmpPoints = extract_data(tb.GetRedAutoAmpPoints, Match)
BlueAutoAmpPoints = extract_data(tb.GetBlueAutoAmpPoints, Match)
RedTeleAmpPoints = extract_data(tb.GetRedTeleAmpPoints, Match)
BlueTeleAmpPoints = extract_data(tb.GetBlueTeleAmpPoints, Match)
RedAutoSpeakerPoints = extract_data(tb.GetRedAutoSpeakerPoints, Match)
BlueAutoSpeakerPoints = extract_data(tb.GetBlueAutoSpeakerPoints, Match)
RedSpeakerPointsRegular = extract_data(tb.GetRedSpeakerPointsRegular, Match)
BlueSpeakerPointsRegular = extract_data(tb.GetBlueSpeakerPointsRegular, Match)
RedTeleSpeakerPointsAmped = extract_data(tb.GetRedTeleSpeakerPointsAmped, Match)
BlueTeleSpeakerPointsAmped = extract_data(tb.GetBlueTeleSpeakerPointsAmped, Match)
RedCenterTrapPoints = extract_data(tb.GetRedCenterTrapPoints, Match)
BlueCenterTrapPoints = extract_data(tb.GetBlueCenterTrapPoints, Match)
RedLeftTrapPoints = extract_data(tb.GetRedLeftTrapPoints, Match)
BlueLeftTrapPoints = extract_data(tb.GetBlueLeftTrapPoints, Match)
RedRightTrapPoints = extract_data(tb.GetRedRightTrapPoints, Match)
BlueRightTrapPoints = extract_data(tb.GetBlueRightTrapPoints, Match)
RedParkStatus1 = extract_data(tb.GetRedParkStatus1, Match)
BlueParkStatus1 = extract_data(tb.GetBlueParkStatus1, Match)
RedParkStatus2 = extract_data(tb.GetRedParkStatus2, Match)
BlueParkStatus2 = extract_data(tb.GetBlueParkStatus2, Match)
RedParkStatus3 = extract_data(tb.GetRedParkStatus3, Match)
BlueParkStatus3 = extract_data(tb.GetBlueParkStatus3, Match)
RedCenterMicStatus = extract_data(tb.GetRedCenterMicStatus, Match)
BlueCenterMicStatus = extract_data(tb.GetBlueCenterMicStatus, Match)
RedLeftMicStatus = extract_data(tb.GetRedLeftMicStatus, Match)
BlueLeftMicStatus = extract_data(tb.GetBlueLeftMicStatus, Match)
RedRightMicStatus = extract_data(tb.GetRedRightMicStatus, Match)
BlueRightMicStatus = extract_data(tb.GetBlueRightMicStatus, Match)
RedHarmonyPoints = extract_data(tb.GetRedHarmonyPoints, Match)
BlueHarmonyPoints = extract_data(tb.GetBlueHarmonyPoints, Match)
RedCoopTry = extract_data(tb.GetRedCoopTry, Match)
BlueCoopTry = extract_data(tb.GetBlueCoopTry, Match)


# BlueTotalAutopts= extract_data(tb.GetBlueAutoPoints, Match)
    
# BluetotalChargeStationPoints= [] #extract_data(tb.GetBlueTotalChargeStationPoints, Match)
    
# BlueAutoStationpts= [] #extract_data(tb.GetBlueAutoChargeStationPoints, Match)
    
# BlueAutoStationlvl= [] #extract_data(tb.GetBlueAutoBridgeState, Match)
    
# BlueAutoPark1= extract_data(tb.GetBlueAutoChargeStationRobot1, Match)

# BlueAutoPark2= extract_data(tb.GetBlueAutoChargeStationRobot2, Match)
    
# BlueAutoPark3= extract_data(tb.GetBlueAutoChargeStationRobot3, Match)

# BlueendGameChargeStationPoints= [] #extract_data(tb.GetBlueEndGameChargeStationPoints, Match)

# BlueendGameBridgeState= extract_data(tb.GetBlueEndGameBridgeState, Match)

# BlueEndgamePark1= extract_data(tb.GetBlueEndGameChargeStationRobot1, Match)
    
# BlueEndgamePark2= extract_data(tb.GetBlueEndGameChargeStationRobot2, Match)
    
# BlueEndgamePark3= extract_data(tb.GetBlueEndGameChargeStationRobot3, Match)

# RedTotalAutopts= extract_data(tb.GetRedAutoPoints, Match)
    
# RedtotalChargeStationPoints= [] #extract_data(tb.GetRedTotalChargeStationPoints, Match)
    
# RedAutoStationpts= [] #extract_data(tb.GetRedAutoChargeStationPoints, Match)
    
# RedAutoStationlvl= [] #extract_data(tb.GetRedAutoBridgeState, Match)
    
# RedAutoPark1= extract_data(tb.GetRedAutoChargeStationRobot1, Match)

# RedAutoPark2= extract_data(tb.GetRedAutoChargeStationRobot2, Match)
    
# RedAutoPark3= extract_data(tb.GetRedAutoChargeStationRobot3, Match)

# RedendGameChargeStationPoints= [] #extract_data(tb.GetRedEndGameChargeStationPoints, Match)

# RedendGameBridgeState= extract_data(tb.GetRedEndGameBridgeState, Match)

# RedEndgamePark1= extract_data(tb.GetRedEndGameChargeStationRobot1, Match)
    
# RedEndgamePark2= extract_data(tb.GetRedEndGameChargeStationRobot2, Match)

# RedEndgamePark3= extract_data(tb.GetRedEndGameChargeStationRobot3, Match)



# sizes = []

# sizes.append(len(BlueRP))
# sizes.append(len(BlueAlliance))
# sizes.append(len(BlueScore))
# sizes.append(len(RedRP))
# sizes.append(len(RedScore))
# sizes.append(len(RedAlliance))
# sizes.append(len(Winner))

# sizes.append(len(BlueTotalAutopts))
# #sizes.append(len(BluetotalChargeStationPoints))
# #sizes.append(len(BlueAutoStationpts))
# #sizes.append(len(BlueAutoStationlvl))
# sizes.append(len(BlueAutoPark1))
# sizes.append(len(BlueAutoPark2))
# sizes.append(len(BlueAutoPark3))
# #sizes.append(len(BlueendGameChargeStationPoints))
# sizes.append(len(BlueendGameBridgeState))
# sizes.append(len(BlueEndgamePark1))
# sizes.append(len(BlueEndgamePark2))
# sizes.append(len(BlueEndgamePark3))

# sizes.append(len(RedTotalAutopts))
# #sizes.append(len(RedtotalChargeStationPoints))
# #sizes.append(len(RedAutoStationpts))
# #sizes.append(len(RedAutoStationlvl))
# sizes.append(len(RedAutoPark1))
# sizes.append(len(RedAutoPark2))
# sizes.append(len(RedAutoPark3))
# #sizes.append(len(RedendGameChargeStationPoints))
# sizes.append(len(RedendGameBridgeState))
# sizes.append(len(RedEndgamePark1))
# sizes.append(len(RedEndgamePark2))
# sizes.append(len(RedEndgamePark3))



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

#blueTeams = inner_lists = BlueAlliance[2:-2].split("'], ['")


#blue_parsed_list = BlueAlliance[1:-1].split("], [")

# Parse the string using literal_eval from the ast module
blue_first_elements = []
blue_second_elements = []
blue_third_elements = []

# Iterate over each inner list and append corresponding elements to their respective lists
for inner_list in BlueAlliance:
    blue_first_elements.append(inner_list[0])
    blue_second_elements.append(inner_list[1])
    blue_third_elements.append(inner_list[2])



#red_parsed_list = RedAlliance[1:-1].split("], [")

# Parse the string using literal_eval from the ast module
red_first_elements = []
red_second_elements = []
red_third_elements = []

# Iterate over each inner list and append corresponding elements to their respective lists
for inner_list in RedAlliance:
    red_first_elements.append(inner_list[0])
    red_second_elements.append(inner_list[1])
    red_third_elements.append(inner_list[2])


 
    
data2 = pd.DataFrame({
    
    "Matches":match,
    "Blue RP": BlueRP,
    "Blue Score": BlueScore,
    "Blue1": blue_first_elements,
    "Blue2": blue_second_elements,
    "Blue3": blue_third_elements,
    "Red RP": RedRP,
    "Red Score": RedScore,
    "Red1": red_first_elements,
    "Red2": red_second_elements,
    "Red3": red_third_elements,
    "Winner": Winner,
    # For Blue Alliance:
    "Blue Coop Try": BlueCoopTry,
    "Blue Auto Points": BlueAutoPoints,
    "Blue Auto Amp Points": BlueAutoAmpPoints,
    "Blue Tele Amp Points": BlueTeleAmpPoints,
    "Blue Auto Speaker Points": BlueAutoSpeakerPoints,
    "Blue Speaker Points Regular": BlueSpeakerPointsRegular,
    "Blue Tele Speaker Points Amped": BlueTeleSpeakerPointsAmped,
    "Blue Center Trap Points": BlueCenterTrapPoints,
    "Blue Left Trap Points": BlueLeftTrapPoints,
    "Blue Right Trap Points": BlueRightTrapPoints,
    "Blue Park Status 1": BlueParkStatus1,
    "Blue Park Status 2": BlueParkStatus2,
    "Blue Park Status 3": BlueParkStatus3,
    "Blue Center Mic Status": BlueCenterMicStatus,
    "Blue Left Mic Status": BlueLeftMicStatus,
    "Blue Right Mic Status": BlueRightMicStatus,
    "Blue Harmony Points": BlueHarmonyPoints,
    

    # For Red Alliance:
    "Red Coop Try": RedCoopTry,
    "Red Auto Points": RedAutoPoints,
    "Red Auto Amp Points": RedAutoAmpPoints,
    "Red Tele Amp Points": RedTeleAmpPoints,
    "Red Auto Speaker Points": RedAutoSpeakerPoints,
    "Red Speaker Points Regular": RedSpeakerPointsRegular,
    "Red Tele Speaker Points Amped": RedTeleSpeakerPointsAmped,
    "Red Center Trap Points": RedCenterTrapPoints,
    "Red Left Trap Points": RedLeftTrapPoints,
    "Red Right Trap Points": RedRightTrapPoints,
    "Red Park Status 1": RedParkStatus1,
    "Red Park Status 2": RedParkStatus2,
    "Red Park Status 3": RedParkStatus3,
    "Red Center Mic Status": RedCenterMicStatus,
    "Red Left Mic Status": RedLeftMicStatus,
    "Red Right Mic Status": RedRightMicStatus,
    "Red Harmony Points": RedHarmonyPoints,
    
    #bro fogor
    "Coopertition Achieve": CoopertitionBonusAchieved,
    

    # "Blue Total Auto pts": BlueTotalAutopts,
    # # "Blue totalChargeStationPoints": BluetotalChargeStationPoints,
    # # "Blue Auto Station pts": BlueAutoStationpts,
    # # "Blue Auto Station lvl": BlueAutoStationlvl,
    # "Blue Auto Park 1": BlueAutoPark1,
    # "Blue Auto Park 2": BlueAutoPark2,
    # "Blue Auto Park 3": BlueAutoPark3,
    # # "Blue endGameChargeStationPoints": BlueendGameChargeStationPoints,
    # "Blue endGameBridgeState": BlueendGameBridgeState,
    # "Blue Endgame Park 1": BlueEndgamePark1,
    # "Blue Endgame Park 2": BlueEndgamePark2,
    # "Blue Endgame Park 3": BlueEndgamePark3,
    # "Red Total Auto pts": RedTotalAutopts,
    # # "Red totalChargeStationPoints": RedtotalChargeStationPoints,
    # # "Red Auto Station pts": RedAutoStationpts,
    # # "Red Auto Station lvl": RedAutoStationlvl,
    # "Red Auto Park 1": RedAutoPark1,
    # "Red Auto Park 2": RedAutoPark2,
    # "Red Auto Park 3": RedAutoPark3,
    # # "Red endGameChargeStationPoints": RedendGameChargeStationPoints,
    # "Red endGameBridgeState": RedendGameBridgeState,
    # "Red Endgame Park 1": RedEndgamePark1,
    # "Red Endgame Park 2": RedEndgamePark2,
    # "Red Endgame Park 3": RedEndgamePark3
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