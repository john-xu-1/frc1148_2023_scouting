import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict, deque  # Added deque import
fun = "/Users/matthewahn/Desktop/"

    # The Scouting Assignment Problem
    #     Problem Description
    #     The Scouting Assignment Problem involves scheduling team members to observe robots during a robotics competition, subject to various constraints. This is fundamentally a constrained optimization problem combining elements of scheduling, resource allocation, and load balancing.
    #     Inputs

    #     List of Scout Names: The team members available for scouting duties
    #     Total Number of Matches: Typically around 74 matches that need coverage
    #     Unavailability Constraints: A mapping of <name, List of unavailable match numbers> indicating when specific scouts cannot participate

    #     Output
    #     A comprehensive scouting schedule represented as a mapping of <Name, matchNumber&robot>, which can be visualized as a table with:

    #     Rows representing match numbers (1 to ~74)
    #     Columns representing the 6 robots (R1, R2, R3, B1, B2, B3)
    #     Cell values containing the name of the assigned scout
    #     Color-coding to indicate scout groupings

    #     Constraints

    #     Complete Coverage: All 6 robots (R1, R2, R3, B1, B2, B3) must be watched during every match
    #     Consecutive Match Limit: A scout can watch a maximum of 10 consecutive matches before requiring a break
    #     Minimum Break Duration: Breaks must last at least 10 matches
    #     Fair Distribution: The difference in total matches watched by each scout should be minimized
    #     Consistency: The number of consecutive matches and non-watched matches should be consistent with an error margin of ±1
    #     Robot Consistency: If possible, a scout should watch the same robot each time they're assigned
    #     Unavailability Respect: Scouts cannot be assigned during their unavailable matches

    #     Additional Requirements

    #     Group Formation: When possible, scouts should be grouped in sizes of 2, 3, or 6 to improve schedule consistency
    #     Visual Representation: The final schedule should be visualized like an Excel sheet with color-coded cells to indicate groupings

# Inputs
scout_names = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Hank']
total_matches = 74
unavailability = {
    'Alice': [1, 2, 3],
    'Bob': [4, 5],
    'Charlie': [10, 11, 12],
}

class ScoutScheduler:
    def __init__(self, scout_names, total_matches, unavailability):
        self.scout_names = scout_names
        self.total_matches = total_matches
        self.unavailability = unavailability
        self.schedule = {m: {r: None for r in ['R1', 'R2', 'R3', 'B1', 'B2', 'B3']} 
                        for m in range(1, total_matches+1)}
        self.scout_data = {
            s: {
                'last_match': -20,
                'consecutive': 0,
                'total': 0,
                'robots': set(),
                'breaks': []
            } for s in scout_names
        }
        
    def is_available(self, scout, match):
        if match in self.unavailability.get(scout, []):
            return False
        if (match - self.scout_data[scout]['last_match']) <= 10:
            return False
        return True
    
    def get_available_scouts(self, match):
        return [s for s in self.scout_names if self.is_available(s, match)]
    
    def assign_robot(self, scout, match, robot):
        self.schedule[match][robot] = scout
        self.scout_data[scout]['last_match'] = match
        self.scout_data[scout]['total'] += 1
        self.scout_data[scout]['robots'].add(robot)
        
    def create_schedule(self):
        for match in range(1, self.total_matches + 1):
            robots = ['R1', 'R2', 'R3', 'B1', 'B2', 'B3']
            assigned = set()
            
            # Get available scouts sorted by workload and robot consistency
            available = sorted(
                self.get_available_scouts(match),
                key=lambda x: (
                    -len(self.scout_data[x]['robots']),  # Prefer scouts with specialized robots
                    self.scout_data[x]['total'],
                    self.scout_data[x]['last_match']
                )
            )
            
            # Emergency fallback with break override
            if len(available) < 6:
                needed = 6 - len(available)
                fallback = sorted(
                    self.scout_names,
                    key=lambda x: (
                        self.scout_data[x]['last_match'],
                        self.scout_data[x]['total']
                    )
                )[:needed]
                available += fallback
            
            # Assign robots with priority to consistent positions
            for robot in robots:
                best_scout = None
                best_score = -float('inf')
                
                for scout in available:
                    if scout in assigned:
                        continue
                        
                    # Calculate priority score
                    score = 0
                    # Penalize for recent work
                    score -= (match - self.scout_data[scout]['last_match']) / 10
                    # Reward for previous work on this robot
                    if robot in self.scout_data[scout]['robots']:
                        score += 2
                    # Penalize for total workload
                    score -= self.scout_data[scout]['total'] * 0.1
                    
                    if score > best_score:
                        best_score = score
                        best_scout = scout
                
                if best_scout:
                    self.assign_robot(best_scout, match, robot)
                    assigned.add(best_scout)
                    available.remove(best_scout)
        
        return self.schedule, {s: self.scout_data[s]['total'] for s in self.scout_names}

def validate_schedule(schedule, scout_load, unavailability, total_matches, scout_names):
    errors = []
    
    # 1. Check complete coverage
    for match in range(1, total_matches + 1):
        for robot in ['R1', 'R2', 'R3', 'B1', 'B2', 'B3']:
            if schedule[match][robot] is None:
                errors.append(f"❌ Incomplete coverage: Match {match} {robot} has no scout")
            elif schedule[match][robot] not in scout_names:
                errors.append(f"❌ Invalid scout: Match {match} {robot} has unknown scout '{schedule[match][robot]}'")

    # 2. Check unavailability constraints
    for scout, matches in unavailability.items():
        for match in matches:
            for robot in ['R1', 'R2', 'R3', 'B1', 'B2', 'B3']:
                if schedule[match][robot] == scout:
                    errors.append(f"❌ Unavailability violation: {scout} was assigned to {robot} in match {match} despite being unavailable")

    # 3. Check single assignment per match
    scout_assignments = defaultdict(lambda: defaultdict(set))
    for match in schedule:
        match_scouts = set()
        for robot, scout in schedule[match].items():
            if scout:
                if scout in match_scouts:
                    errors.append(f"❌ Double assignment: {scout} assigned to multiple robots in match {match}")
                match_scouts.add(scout)
                scout_assignments[scout][match].add(robot)

    # 4. Check consecutive matches and breaks
    consecutive_tracker = {scout: [] for scout in scout_names}
    for scout in scout_names:
        matches = sorted([m for m in scout_assignments[scout] if scout_assignments[scout][m]])
        if not matches:
            continue
            
        current_streak = [matches[0]]
        for i in range(1, len(matches)):
            if matches[i] == current_streak[-1] + 1:
                current_streak.append(matches[i])
            else:
                if len(current_streak) > 10:
                    errors.append(f"❌ Consecutive matches exceeded: {scout} worked {len(current_streak)} matches in a row (matches {current_streak[0]}-{current_streak[-1]})")
                current_streak = [matches[i]]
        
        # Check final streak
        if len(current_streak) > 10:
            errors.append(f"❌ Consecutive matches exceeded: {scout} worked {len(current_streak)} matches in a row (matches {current_streak[0]}-{current_streak[-1]})")

        # Check breaks between assignments
        for i in range(1, len(matches)):
            gap = matches[i] - matches[i-1]
            if 1 < gap <= 10:  # Break too short but not consecutive
                errors.append(f"❌ Insufficient break: {scout} had only {gap-1} match break between matches {matches[i-1]} and {matches[i]}")

    # 5. Check fair distribution
    avg_matches = total_matches * 6 / len(scout_names)
    min_load = min(scout_load.values())
    max_load = max(scout_load.values())
    if max_load - min_load > 1:
        errors.append(f"❌ Unfair distribution: Load varies from {min_load} to {max_load} (max difference should be ≤1)")

    # 6. Check robot consistency (if possible)
    robot_consistency = defaultdict(set)
    for scout in scout_names:
        for match in scout_assignments[scout]:
            for robot in scout_assignments[scout][match]:
                robot_consistency[scout].add(robot)
        if len(robot_consistency[scout]) > 1:
            errors.append(f"⚠️ Robot inconsistency: {scout} watched {len(robot_consistency[scout])} different robots")

    if errors:
        print("\n".join(errors))
        print(f"\nFound {len(errors)} validation errors!")
        return False, "\n".join(errors)
    
    return True, "✅ Schedule is valid!"

def assign_groups_and_colors(schedule, scout_names):
    from collections import defaultdict

    # Track which robots each scout is assigned to
    scout_robots = defaultdict(set)
    for match in schedule.values():
        for robot, scout in match.items():
            if scout:
                scout_robots[scout].add(robot)

    # Group scouts who watch the same robots
    groups = []
    used_scouts = set()
    for scout in scout_names:
        if scout not in used_scouts:
            # Find all scouts who watch the same set of robots
            group = [s for s in scout_names if scout_robots[s] == scout_robots[scout]]
            groups.append(tuple(group))
            used_scouts.update(group)

    # Assign colors to groups
    colors = ['#FFD700', '#87CEEB', '#90EE90', '#FFA07A', '#E6E6FA', '#FFDAB9', '#ADD8E6', '#FFC0CB']
    group_colors = {}
    for i, group in enumerate(groups):
        group_colors[group] = f"Group {i + 1}"

    return groups, group_colors

def create_schedule_image(schedule_df, groups, group_colors, filename="scouting_schedule.png"):
    # Create a figure and axis
    fig_width = max(12, schedule_df.shape[1] * 1.5)
    fig_height = max(8, schedule_df.shape[0] * 0.3)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    
    # Hide the axes
    ax.axis('tight')
    ax.axis('off')
    
    # Create color mapping for groups
    colors = ['#FFD700', '#87CEEB', '#90EE90', '#FFA07A', '#E6E6FA', '#FFDAB9', '#ADD8E6', '#FFC0CB']
    color_map = {}
    
    for group, group_name in group_colors.items():
        color_hash = hash(group_name) % len(colors)
        for scout in group:
            color_map[scout] = colors[color_hash]
    
    # Create cell colors array
    cell_colors = np.full((schedule_df.shape[0], schedule_df.shape[1]), 'white', dtype=object)
    
    # Fill in colors based on group membership
    for i in range(schedule_df.shape[0]):
        for j in range(1, schedule_df.shape[1]):  # Skip match number column
            val = schedule_df.iloc[i, j]
            if pd.notna(val) and val in color_map:
                cell_colors[i, j] = color_map[val]
    
    # Create the table
    table = ax.table(
        cellText=schedule_df.values,
        colLabels=schedule_df.columns,
        cellColours=cell_colors,
        cellLoc='center',
        loc='center'
    )
    
    # Adjust table properties
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.2)
    
    # Add a title
    plt.title('Scouting Assignment Schedule', fontsize=16, pad=20)
    
    # Add legend for groups
    legend_elements = []
    for group_tuple, group_name in group_colors.items():
        color_hash = hash(group_name) % len(colors)
        patch = plt.Rectangle((0, 0), 1, 1, fc=colors[color_hash])
        legend_elements.append((patch, f"{group_name}: {', '.join(group_tuple)}"))
    
    if legend_elements:
        patches, labels = zip(*legend_elements)
        plt.legend(patches, labels, loc='upper center', bbox_to_anchor=(0.5, 0), 
                   ncol=min(3, len(legend_elements)), frameon=True)
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight', dpi=150)
    plt.close()
    
    print(f"Schedule visualization saved to '{filename}'")

def main():
    scheduler = ScoutScheduler(scout_names, total_matches, unavailability)
    schedule, scout_load = scheduler.create_schedule()
    is_valid, message = validate_schedule(schedule, scout_load, unavailability, total_matches, scout_names)
    
    if is_valid:
        schedule_df = pd.DataFrame.from_dict(schedule, orient='index')
        groups, group_colors = assign_groups_and_colors(schedule, scout_names)
        create_schedule_image(schedule_df, groups, group_colors)
    else:
        print("Schedule validation failed. Reasons:")
        print(message)

if __name__ == "__main__":
    main()