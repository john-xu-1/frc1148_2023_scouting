import pygsheets
import pandas as pd
import TBA_Functions as tb
import CalculateOPR as cop
import numpy as np
import re
import re
import ast
from collections import Counter
from datetime import datetime

# Logic for this is that since the most recent event is the division of worlds that they are going to
# we want to get the second most recent event that they are going to.

# If the last event they went to also had a division (like how the divisions -> Einstein)
# we want to get the event code of the third most recent event that they went to in order to get all the data

print("starting")
teamNumbers = [
"7457", "3005", "6329", "1771", "359", "1706", "3276", "88", "3663", "27", "67", "2046", "4481", "4611", "3478", "5813", "3467", "3175", "8884", "4020", "862", "8608", "3539", "9442", "7166", "340", "2847", "5460", "6615", "103", "8513", "870", "9609", "1391", "4237", "4795", "1261", "469", "5804", "4646", "166", "1498", "7028", "4422", "1073", "1148", "5530", "3061", "3313", "2022", "3100", "6941", "75", "4534", "3501", "9401", "858", "6421", "6838", "3487", "4192", "6948", "3354", "4256", "7657", "2642", "1466", "5112", "6352", "5654", "2640", "1329", "10656", "10518", "10032"
]

lastEvent = []
incomp = []

def getactualLastevent(status):

    # Assuming `status` is your list of dictionaries (the JSON data)

    # Sort by start_date in descending order (most recent first)
    sorted_events = sorted(status, key=lambda x: datetime.strptime(x["start_date"], "%Y-%m-%d"), reverse=True)

    # Get the second to most recent start_date event
    second_most_recent = sorted_events[1]

    # Get the first_event_code and return "2025" + first_event_code
    result = "2025" + second_most_recent["event_code"]

    return(result)

def actualLasteventIfDivision(status):
     sorted_events = sorted(status, key=lambda x: datetime.strptime(x["start_date"], "%Y-%m-%d"), reverse=True)
     third_most_recent = sorted_events[2]
     result = "2025" + third_most_recent["event_code"]
     return(result)
    
def hasdivision(json):
    if json["division_keys"] != []:
        return True

for teamNumber in teamNumbers:
    theKeys = tb.getLastEvent(teamNumber)
    actualLastevent = getactualLastevent(theKeys)    
    actualLasteventIfDivisionkey = actualLasteventIfDivision(theKeys)
    if hasdivision(tb.getEventDivisionInfo(actualLastevent)):
        lastEvent.append(actualLasteventIfDivisionkey)
    else:
        lastEvent.append(actualLastevent)


print("Events in order")
print (lastEvent)