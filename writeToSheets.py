import pygsheets
import pandas as pd
import TBA_Functions as tb
import CalculateOPR as cop
import numpy as np
import re
import re
import ast
from collections import Counter

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
curEvent = "2024catt"

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

OPRAll = tb.TBA_EventOPRs(curEvent)

OPR = list(OPRAll['oprs'].values())

DPR = list(OPRAll['dprs'].values())

CCWM = list(OPRAll['ccwms'].values())

# Teams = tb.TBA_EventTeamsFormatted(curEvent)
Teams = list(OPRAll['ccwms'].keys())

speakerNAmps = cop.coneNcubeOPR(event=curEvent)

matchesPlayed = []

sh = gc.open('Scouting Spreadsheet')
wks = sh[5]

rows = wks.get_all_values()

#code added to get matches played from App results
teamIsoColumn = [row[23] for row in rows[1:]]
teamCounts = Counter(teamIsoColumn)

avgAmpNum = {}
avgSpeakerNum = {}
avgMissedSpeaker = {}
avgMissedAmp = {}
teamMatches = {}
passNum = {}
nickNames = []
climbFailNum = {}
climbTryNum = {}
trapScoredNum = {}
trapMissedNum = {}
breakNum = {}

print (Teams)

for row in rows[1:]:
    name = row[0]
    intBoolValue = 0
    if name != '':
        
        cutoff = name.index("c")
        name = name[cutoff+1:]
        if name in Teams:  
            print (row)
            if row[5] != '':
                if name not in avgAmpNum:
                    avgAmpNum[name] = 0
                avgAmpNum[name] += int(row[5])
                print (avgAmpNum[name]) 
            if row[3] != '':
                if name not in avgSpeakerNum:
                    avgSpeakerNum[name] = 0
                avgSpeakerNum[name] += int(row[3])
            if row[4] != '':
                if name not in avgSpeakerNum:
                    avgSpeakerNum[name] = 0
                avgSpeakerNum[name] += int(row[4])
            if row[7] != '':
                if name not in avgMissedSpeaker:
                    avgMissedSpeaker[name] = 0
                avgMissedSpeaker[name] += int(row[7])
                print (avgMissedSpeaker[name])
            if row[12] != '':
                if name not in passNum:
                    passNum[name] = 0
                passNum[name] += int(row[12])
            if row[6] != '':
                if name not in trapScoredNum:
                    trapScoredNum[name] = 0
                trapScoredNum[name] += ((int (row[6]))/5)
            if row[9] != '':
                if name not in trapMissedNum:
                    trapMissedNum[name] = 0
                trapMissedNum[name] += int(row[9])
            if row[10] != '':
                if name not in climbTryNum:
                    climbTryNum[name] = 0
                if row[10] == "TRUE":
                    intBoolValue = 1
                if row[10] == "FALSE":
                    intBoolValue = 0
                climbTryNum[name] += intBoolValue
            if row[11] != '':
                if name not in climbFailNum:
                    climbFailNum[name] = 0
                if row[11] == "TRUE":
                    intBoolValue = 1
                if row[11] == "FALSE":
                    intBoolValue = 0
                climbFailNum[name] += intBoolValue
            if row[15] != '':
                if name not in breakNum:
                    breakNum[name] = 0
                if row[15] == "TRUE":
                    intBoolValue = 1
                if row[15] == "FALSE":
                    intBoolValue = 0
                breakNum[name] += intBoolValue
            if row[8] != '':
                if name not in avgMissedAmp:
                    avgMissedAmp[name] = 0
                avgMissedAmp[name] += int(row[8])
            if name not in teamMatches:
                teamMatches[name] = 0
            teamMatches[name] += 1

print(avgSpeakerNum)     
print (str(len(teamMatches)) + "============")
# print (avgAmpNum)
# print (avgSpeakerNum)



#values = result.get("values", [])


# OPR = []
# DPR = []
# CCWM = []
# winRates = []
ampOPR = []
speakerOPR = []
Amps = []
Speakers = []


print (len(Teams))


winRates = []

for team in Teams:
    print(team)
    if (tb.TBA_TeamEventStatus(team, curEvent) is not None) or (team[len(team) - 1] == 'B'):
        matchesPlayed.append(teamCounts[team])
    else:
        matchesPlayed.append("3")
    if team not in avgAmpNum:
        avgAmpNum[team] = 0
    if team not in avgSpeakerNum:
        avgSpeakerNum[team] = 0
    if team not in avgMissedSpeaker:
        avgMissedSpeaker[team] = 0
        print ("set missed = 0 ", team)
    if team not in avgMissedAmp:
        avgMissedAmp[team] = 0
    if team not in teamMatches:
        teamMatches[team] = 0
    if team[len(team)-1] == 'B':
        theCurrentName = tb.TBA_TeamNickname(team[3:len(team)-1]) + " B team"
        nickNames.append(theCurrentName)
    else:
        theCurrentName = tb.TBA_TeamNickname(team[3:])
        nickNames.append(theCurrentName)
    # OPR.append( 0)
    # DPR.append( 0)
    # CCWM.append( 0)
    #winRates.append( 0)
    ampOPR.append( 0)
    speakerOPR.append( 0)
    Amps.append( 0)
    Speakers.append( 0)


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
sortedAmpNum = sorted(avgAmpNum.items(), key=lambda x: Teams.index(x[0]) if x[0] in Teams else float('inf'))
sortedSpeakerNum = sorted(avgSpeakerNum.items(), key=lambda x: Teams.index(x[0]) if x[0] in Teams else float('inf'))
sortedMissedSpeaker = sorted(avgMissedSpeaker.items(), key=lambda x: Teams.index(x[0]) if x[0] in Teams else float('inf'))
sortedMissedAmp = sorted(avgMissedAmp.items(), key=lambda x: Teams.index(x[0]) if x[0] in Teams else float('inf'))
sortedTeamMatches = sorted(teamMatches.items(), key=lambda x: Teams.index(x[0]) if x[0] in Teams else float('inf'))
sortedPassNum = sorted(passNum.items(), key=lambda x: Teams.index(x[0]) if x[0] in Teams else float('inf'))
sortedClimbFailNum = sorted(climbFailNum.items(), key=lambda x: Teams.index(x[0]) if x[0] in Teams else float('inf'))
sortedClimbTryNum = sorted(climbTryNum.items(), key=lambda x: Teams.index(x[0]) if x[0] in Teams else float('inf'))
sortedTrapScoredNum = sorted(trapScoredNum.items(), key=lambda x: Teams.index(x[0]) if x[0] in Teams else float('inf'))
sortedTrapMissedNum = sorted(trapMissedNum.items(), key=lambda x: Teams.index(x[0]) if x[0] in Teams else float('inf'))
sortedBreakNum = sorted(breakNum.items(), key=lambda x: Teams.index(x[0]) if x[0] in Teams else float('inf'))
# print (len(sortedAmpNum))
# print (sortedAmpNum[0])
# print (sortedAmpNum[0][1])
# print (len (sortedSpeakerNum))
# # sortedSpeakerNumArray = []
# # for item in sortedSpeakerNum:
# #     sortedSpeakerNumArray.append( item[1] )
# # sortedAmpNumArray = []
# # for item in sortedAmpNum:
# #     sortedAmpNumArray.append( item[1] )
# print (len([item[1] for item in sortedSpeakerNum] ))
# print (len([item[1] for item in sortedAmpNum] ))
# print (sortedMissedSpeaker)
# print (sortedAmpNum)
# print (sortedMissedAmp)
# print (sortedMissedSpeaker)


print (len(Teams))
#OPR.append(0)
print (len(OPR[:48]))
#DPR.append (0)
print (len(DPR[:48]))
#CCWM.append (0)
print (len(CCWM[:48]))
print (len(winRates))
# print (len(speakerNAmps["ampOPR"]))
# print (len(speakerNAmps["speakerOPR"]))
# print (len(matchesPlayed))
# print (len(speakerNAmps["Amps"]))
# print (len(speakerNAmps["Speakers"]))
print (len(sortedAmpNum))                         
print (len(sortedSpeakerNum))
print (len(sortedMissedSpeaker))
print (len(sortedMissedAmp))

print (type(Teams))

print (len(speakerNAmps["ampOPR"]))
print (len(speakerNAmps["speakerOPR"]))

##changed the OPR[:36], "DPR":DPR[:36], "CCWM":CCWM[:36], to 47
#:50 for 50 teams in current event
#data = pd.DataFrame({"Teams":Teams,"OPR":OPR[:50], "DPR":DPR[:50], "CCWM":CCWM[:50], "Win Rate %": winRates, "Amp OPR": ampOPR, "Speaker OPR": speakerOPR, "Matches Played": teamMatches, "Amps per Game": Amps, "Speaker per Game": Speakers, "Team Total Speaker": [item[1] for item in sortedSpeakerNum], "Team Total Amp": [item[1] for item in sortedAmpNum], "Total Missed Speaker": [item[1] for item in sortedMissedSpeaker], "Total Missed Amp": [item[1] for item in sortedMissedAmp],})
data = pd.DataFrame({"Teams":Teams,
                     "OPR":OPR[:48], 
                     "DPR":DPR[:48], 
                     "CCWM":CCWM[:48], 
                     "Win Rate %": winRates, 
                     "Amp OPR": speakerNAmps["ampOPR"], 
                     "Speaker OPR": speakerNAmps["speakerOPR"], 
                     "Matches Played": [item[1] for item in sortedTeamMatches], 
                     "Amps per Game(OPR)": speakerNAmps["AmpsCount"], 
                     "Speaker per Game(OPR)": speakerNAmps["SpeakersCount"], 
                     "Team Total Speaker": [item[1] for item in sortedSpeakerNum], 
                     "Team Total Amp": [item[1] for item in sortedAmpNum], 
                     "Total Missed Speaker": [item[1] for item in sortedMissedSpeaker], 
                     "Total Missed Amp": [item[1] for item in sortedMissedAmp],})
# "Amp OPR": speakerNAmps["ampOPR"], "Speaker OPR": speakerNAmps["speakerOPR"], "Matches Played": matchesPlayed, "Amps per Game": speakerNAmps["Amps"], "Speaker per Game": speakerNAmps["Speakers"],
print ("start power rating data")
sh = gc.open('Scouting Spreadsheet')
wks = sh[1]
wks.set_dataframe(data,(1,1))

data = pd.DataFrame({
    "Total Passes": [item[1] for item in sortedPassNum],
    "Climb Fails": [item[1] for item in sortedClimbFailNum],
    "Climb Tries": [item[1] for item in sortedClimbTryNum],
    "Trap Scored": [item[1] for item in sortedTrapScoredNum],
    "Trap Missed": [item[1] for item in sortedTrapMissedNum],
    "Total Breaks": [item[1] for item in sortedBreakNum]
})



wks.set_dataframe(data,(1,22))

data = pd.DataFrame({
    "Team Name": nickNames,
})
wks.set_dataframe(data,(1,33))
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

MatchJsonfile = EventMatchKeys(curEvent)## Match info
matchKeysForListin = tb.TBA_EventMatchKeys(curEvent)## Match keys


# Sort the list by category (qm, sf, f) and then by the number within each category
matchKeysForListin = custom_sort(matchKeysForListin)#this is the match keys
MatchJsonfile = custom_sort_M(MatchJsonfile)#this is the Json of the match
print (MatchJsonfile)


#BlueRP, BlueScore, BlueAlliance, RedAlliance, RedRP, RedScore, BlueTotalAutopts, BluetotalChargeStationPoints, BlueAutoStationpts, BlueAutoStationlvl, BlueAutoPark1, BlueAutoPark2, BlueAutoPark3, BlueEndgamePark1, BlueEndgamePark2, BlueEndgamePark3, Winner = []
#RedTotalAutopts, RedtotalChargeStationPoints, RedAutoStationpts, RedAutoStationlvl, RedeAutoPark1, RedAutoPark2, RedAutoPark3, RedEndgamePark1, RedEndgamePark2, RedEndgamePark3 = []  

# CoopertitionBonusAchieved = extract_data(tb.GetCoopertitionBonusAchieved,Match)

BlueRP = extract_data(tb.GetBlueRP, MatchJsonfile)

BlueScore= extract_data(tb.GetBlueScore, MatchJsonfile)

BlueAlliance= extract_data(tb.GetBlueTeams, MatchJsonfile)

RedAlliance= extract_data(tb.GetRedTeams, MatchJsonfile)

RedRP= extract_data(tb.GetRedRP, MatchJsonfile)

RedScore = extract_data(tb.GetRedScore, MatchJsonfile)

Winner = extract_data(tb.TBA_MatchWinner, MatchJsonfile)

RedAutoPoints = extract_data(tb.GetRedAutoPoints, MatchJsonfile)
BlueAutoPoints = extract_data(tb.GetBlueAutoPoints, MatchJsonfile)
RedRP = extract_data(tb.GetRedRP, MatchJsonfile)
BlueRP = extract_data(tb.GetBlueRP, MatchJsonfile)
RedScore = extract_data(tb.GetRedScore, MatchJsonfile)
BlueScore = extract_data(tb.GetBlueScore, MatchJsonfile)
RedTeams = extract_data(tb.GetRedTeams, MatchJsonfile)
BlueTeams = extract_data(tb.GetBlueTeams, MatchJsonfile)
RedAutoAmpPoints = extract_data(tb.GetRedAutoAmpPoints, MatchJsonfile)
BlueAutoAmpPoints = extract_data(tb.GetBlueAutoAmpPoints, MatchJsonfile)
RedTeleAmpPoints = extract_data(tb.GetRedTeleAmpPoints, MatchJsonfile)
BlueTeleAmpPoints = extract_data(tb.GetBlueTeleAmpPoints, MatchJsonfile)
RedAutoSpeakerPoints = extract_data(tb.GetRedAutoSpeakerPoints, MatchJsonfile)
BlueAutoSpeakerPoints = extract_data(tb.GetBlueAutoSpeakerPoints, MatchJsonfile)
RedSpeakerPointsRegular = extract_data(tb.GetRedSpeakerPointsRegular, MatchJsonfile)
BlueSpeakerPointsRegular = extract_data(tb.GetBlueSpeakerPointsRegular, MatchJsonfile)
RedTeleSpeakerPointsAmped = extract_data(tb.GetRedTeleSpeakerPointsAmped, MatchJsonfile)
BlueTeleSpeakerPointsAmped = extract_data(tb.GetBlueTeleSpeakerPointsAmped, MatchJsonfile)
RedCenterTrapPoints = extract_data(tb.GetRedCenterTrapPoints, MatchJsonfile)
BlueCenterTrapPoints = extract_data(tb.GetBlueCenterTrapPoints, MatchJsonfile)
RedLeftTrapPoints = extract_data(tb.GetRedLeftTrapPoints, MatchJsonfile)
BlueLeftTrapPoints = extract_data(tb.GetBlueLeftTrapPoints, MatchJsonfile)
RedRightTrapPoints = extract_data(tb.GetRedRightTrapPoints, MatchJsonfile)
BlueRightTrapPoints = extract_data(tb.GetBlueRightTrapPoints, MatchJsonfile)
RedParkStatus1 = extract_data(tb.GetRedParkStatus1, MatchJsonfile)
BlueParkStatus1 = extract_data(tb.GetBlueParkStatus1, MatchJsonfile)
RedParkStatus2 = extract_data(tb.GetRedParkStatus2, MatchJsonfile)
BlueParkStatus2 = extract_data(tb.GetBlueParkStatus2, MatchJsonfile)
RedParkStatus3 = extract_data(tb.GetRedParkStatus3, MatchJsonfile)
BlueParkStatus3 = extract_data(tb.GetBlueParkStatus3, MatchJsonfile)
RedCenterMicStatus = extract_data(tb.GetRedCenterMicStatus, MatchJsonfile)
BlueCenterMicStatus = extract_data(tb.GetBlueCenterMicStatus, MatchJsonfile)
RedLeftMicStatus = extract_data(tb.GetRedLeftMicStatus, MatchJsonfile)
BlueLeftMicStatus = extract_data(tb.GetBlueLeftMicStatus, MatchJsonfile)
RedRightMicStatus = extract_data(tb.GetRedRightMicStatus, MatchJsonfile)
BlueRightMicStatus = extract_data(tb.GetBlueRightMicStatus, MatchJsonfile)
RedHarmonyPoints = extract_data(tb.GetRedHarmonyPoints, MatchJsonfile)
BlueHarmonyPoints = extract_data(tb.GetBlueHarmonyPoints, MatchJsonfile)
# RedCoopTry = extract_data(tb.GetRedCoopTry, Match)
# BlueCoopTry = extract_data(tb.GetBlueCoopTry, Match)


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
    
    "Matches":matchKeysForListin,
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
    # "Blue Coop Try": BlueCoopTry,
    "Blue Coop Try": "Not doing this",
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
    # "Red Coop Try": RedCoopTry,
    "Red Coop Try": "Not doing this",
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
    # "Coopertition Achieve": CoopertitionBonusAchieved,
    

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

print(teamCounts)
print("all done")