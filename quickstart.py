import pygsheets
import pandas as pd
#authorization
curEvent = "2023cala"

gc = pygsheets.authorize(service_file='credentials.json')

# Create empty dataframe
df = pd.DataFrame()

# Create a column
df['name'] = ['John', 'Mathew', 'Sarah']

#open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sh = gc.open('Scouting Spreadsheet')

#select the first sheet 
wks = sh[0]

#update the first sheet with df, starting at cell B2. 
wks.set_dataframe(df,(1,1))

print("starting")
wks = sh[1]

from TBA_Functions import TBA_EventTeamsFormatted
Teams = TBA_EventTeamsFormatted(curEvent)


# data = pd.DataFrame()
# data['points per match']=
# sh = gc.open('Scouting Spreadsheet')
# wks = sh[1]
# wks.set_dataframe(data,(1,1))

from TBA_Functions import TBA_EventOPR
OPR = TBA_EventOPR(curEvent)


# OPR-station

# one points per match

# data['OPR-cone


# cube points per match

# OPR-cube

from TBA_Functions import TBA_EventDPR
DPR = TBA_EventDPR(curEvent)

from TBA_Functions import TBA_EventCCWM
CCWM = TBA_EventCCWM(curEvent)


from TBA_Functions import TBA_WinRate
winRates = []
for i in range (len(Teams)):
   winRates.append( TBA_WinRate(Teams[i],curEvent))

data = pd.DataFrame({"Teams":Teams,"OPR":OPR, "DPR":DPR, "CCWM":CCWM, "Win Rate %": winRates})
sh = gc.open('Scouting Spreadsheet')
wks = sh[1]
wks.set_dataframe(data,(1,1))
print("all done")