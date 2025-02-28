import pandas as pd
import numpy as np

def generate_scouting_schedule(scout_names, total_matches, unavailability, breaks):
    robots = ['R1', 'R2', 'R3', 'B1', 'B2', 'B3']
    num_robots = len(robots)
    num_scouts = len(scout_names)
    
    # Initialize the schedule
    schedule = pd.DataFrame(index=range(1, total_matches + 1), columns=robots)
    schedule[:] = np.nan
    
    # Initialize scout counters
    consecutive_matches = {scout: 0 for scout in scout_names}
    last_assigned = {scout: -1 for scout in scout_names}
    
    # Assign scouts to matches
    for match in range(1, total_matches + 1):
        for robot in robots:
            # Find available scouts
            available_scouts = [scout for scout in scout_names if match not in unavailability.get(scout, [])]
            
            # Prioritize scouts with the least consecutive matches and longest break
            available_scouts.sort(key=lambda x: (consecutive_matches[x], last_assigned[x]))
            
            # Assign the first available scout
            assigned_scout = available_scouts[0]
            schedule.at[match, robot] = assigned_scout
            
            # Update counters
            consecutive_matches[assigned_scout] += 1
            last_assigned[assigned_scout] = match
            
            # Reset consecutive counters if a break occurs
            if match in breaks:
                for scout in scout_names:
                    consecutive_matches[scout] = 0
    
    return schedule



# Example Input
scout_names = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 
               'Grace', 'Hank', 'Ivy', 'Jack']
total_matches = 74
unavailability = {
    'Alice': [1, 2, 3],
    'Bob': [4, 5],
    'Charlie': [10, 11, 12],
}
breaks = [22, 55]  # Optional breaks after matches 22 and 55

# Generate the schedule
schedule = generate_scouting_schedule(scout_names, total_matches, unavailability, breaks)

# Display the schedule
print(schedule)

def color_coding(val):
    color = 'lightblue' if val == 'Alice' else \
            'lightgreen' if val == 'Bob' else \
            'lightcoral' if val == 'Charlie' else \
            'lightyellow' if val == 'David' else \
            'lightpink' if val == 'Eve' else \
            'lightgray' if val == 'Frank' else \
            'lightcyan' if val == 'Grace' else \
            'lightseagreen' if val == 'Hank' else \
            'lightsteelblue' if val == 'Ivy' else \
            'lightsalmon' if val == 'Jack' else ''
    return f'background-color: {color}'

styled_schedule = schedule.style.applymap(color_coding)
styled_schedule

# print(styled_schedule)