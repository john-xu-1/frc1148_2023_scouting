import pygsheets
import pandas as pd
#authorization
gc = pygsheets.authorize(service_file='credentials.json')

# Create empty dataframe
df = pd.DataFrame()

# Create a column
df['name'] = ['John', 'James', 'Sarah']

#open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sh = gc.open('Scouting Spreadsheet')

#select the first sheet 
wks = sh[0]

#update the first sheet with df, starting at cell B2. 
wks.set_dataframe(df,(1,1))

# Create_Service('credentials.json', 'sheets', 'v4',['https://www.googleapis.com/auth/spreadsheets'])      
# from TBA_Functions import TBA_EventTeamsFormatted
# data = TBA_EventTeamsFormatted(curEvent)
# data_pd = pd.DataFrame(data)
# SAMPLE_RANGE_NAME = 'PowerRatings.py!A2:A'

# def Export_Data_To_Sheets():
#     response_date = service.spreadsheets().values().update(
#         spreadsheetId=SAMPLE_SPREADSHEET_ID,
#         valueInputOption='RAW',
#         range=SAMPLE_RANGE_NAME,
#         body=dict(
#             majorDimension='ROWS',
#             values=data_pd.values.tolist())
#     ).execute()
#     print('Sheet successfully Updated')


# Export_Data_To_Sheets()

# from TBA_Functions import TBA_EventOPR
# data = TBA_EventOPR(curEvent)
# data_pd = pd.DataFrame(data)
# SAMPLE_RANGE_NAME = 'PowerRatings.py!C2:C'
# Export_Data_To_Sheets()

# from TBA_Functions import TBA_EventDPR
# data = TBA_EventDPR(curEvent)
# data_pd = pd.DataFrame(data)
# SAMPLE_RANGE_NAME = 'PowerRatings.py!I2:I'
# Export_Data_To_Sheets()

# from TBA_Functions import TBA_EventCCWM
# data = TBA_EventCCWM(curEvent)
# data_pd = pd.DataFrame(data)
# SAMPLE_RANGE_NAME = 'PowerRatings.py!J2:J'
# Export_Data_To_Sheets()