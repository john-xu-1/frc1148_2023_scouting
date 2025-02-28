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
#     Consecutive Match Limit: Will be dicussed below
#     Minimum Break Duration: Will be dicussed below
#     Fair Distribution: The difference in total matches watched by each scout should be minimized
#     Consistency: The number of consecutive matches and non-watched matches should be consistent with an error margin of ±1
#     Robot Consistency: If possible, a scout should watch the same robot each time they're assigned
#     Unavailability Respect: Scouts cannot be assigned during their unavailable matches

# Consecutive Match Limit: Will be dicussed below
# Minimum Break Duration: Will be dicussed below
# Instead of the current way where consecutive match limit is 10 and minimum break duration is 10
# take the number of robots = 6 and miltipy by number of matches = 74 to get total number of matches = 444
# then take the number of watchers = 8 and divide 444/8 = 55.5
# this means that a watcher has to watch ~55 matches and has ~20 breaks
# IT coulkd be split into 27 20 28
# it would be better to have split into somthing like 12 6 13 7 12 7 13
# This isn't a great arrangment but consecutive matches are minimized towards 10, while breaks are maximized to give enough space
# Lets say there are 10 people not 8, then 444/10 = 44.4 and there are ~30 matches of break
# The time can easily be split into somthing like 12 10b 11 10b 11 10b 11
# So the system should use soe sort of math to determine the best way to split the time by looking at ratio or breaks to matches
# and then split the time in a way that is most efficient

# Lets assume that the minimum number of people is 10 and after deciding how breaks adn matches work, fit people into the schedule according to requirments

#     Additional Requirements
#     Group Formation: When possible, scouts should be grouped in sizes of 2, 3, or 6 to improve schedule consistency
#     Visual Representation: The final schedule should be visualized like an Excel sheet with color-coded cells to indicate groupings

import pandas as pd
from collections import defaultdict, deque
import matplotlib.pyplot as plt
import numpy as np

class FlexibleScoutScheduler:
    def __init__(self, scout_names, total_matches, unavailability, 
                 target_consecutive=10, target_break=10):
        self.scout_names = scout_names
        self.total_matches = total_matches
        self.unavailability = unavailability
        self.target_consecutive = target_consecutive
        self.target_break = target_break
        self.robots = ['R1', 'R2', 'R3', 'B1', 'B2', 'B3']
        self.total_shifts = total_matches * len(self.robots)
        
        # Calculate target assignments per scout
        self.num_scouts = len(scout_names)
        self.base_assignments = self.total_shifts // self.num_scouts
        self.extra_assignments = self.total_shifts % self.num_scouts
        
        # Initialize data structures
        self.schedule = {m: {r: None for r in self.robots} 
                        for m in range(1, total_matches + 1)}
        self.scout_data = {s: {
            'work_periods': [],
            'primary_robot': self.robots[i % len(self.robots)],
            'assignments': 0,
            'assigned_robot': defaultdict(int),
            'last_match': -self.target_break  # Track last assignment
        } for i, s in enumerate(scout_names)}

    def generate_work_schedule(self):
        """Improved work period generation with break awareness"""
        assignments_per_scout = {}
        for i, scout in enumerate(self.scout_names):
            assignments = self.base_assignments + (1 if i < self.extra_assignments else 0)
            assignments_per_scout[scout] = assignments
            
            work_schedule = []
            current_match = 1
            remaining = assignments
            
            while remaining > 0 and current_match <= self.total_matches:
                # Calculate ideal block size
                block_size = min(
                    remaining,
                    self.target_consecutive,
                    self.total_matches - current_match + 1
                )
                
                # Find next available block
                while True:
                    end_match = current_match + block_size - 1
                    unavailable_matches = [m for m in range(current_match, end_match+1)
                            if m in self.unavailability.get(scout, [])]
                    
                    if not unavailable_matches:
                        break
                    
                    # Jump to first available match after conflict
                    current_match = max(unavailable_matches) + 1
                    block_size = min(remaining, self.target_consecutive)
                
                # Add break buffer between blocks
                if work_schedule:
                    last_end = work_schedule[-1][1]
                    current_match = max(current_match, last_end + self.target_break + 1)
                
                work_schedule.append((current_match, end_match))
                remaining -= block_size
                current_match = end_match + 1  # Start next block immediately
                
            self.scout_data[scout]['work_periods'] = work_schedule

    def assign_robots(self):
        """Assign scouts to robots with flexibility in constraints."""
        # Create availability timeline
        scout_availability = defaultdict(list)
        for scout in self.scout_names:
            for start, end in self.scout_data[scout]['work_periods']:
                for match in range(start, end + 1):
                    if match <= self.total_matches and match not in self.unavailability.get(scout, []):
                        scout_availability[match].append(scout)

        # Process each match individually
        for match in range(1, self.total_matches + 1):
            available_scouts = scout_availability.get(match, [])
            robot_prefs = {r: [] for r in self.robots}

            # Sort scouts by their affinity to each robot
            for scout in available_scouts:
                primary = self.scout_data[scout]['primary_robot']
                robot_prefs[primary].append(scout)
                
                # Also consider secondary preferences
                other_robots = [r for r in self.robots if r != primary]
                for r in other_robots:
                    robot_prefs[r].append(scout)

            # Create cost matrix for optimal assignment
            cost_matrix = []
            for robot in self.robots:
                row = []
                for scout in available_scouts:
                    # Cost based on previous assignments and preferences
                    cost = (
                        0 if robot == self.scout_data[scout]['primary_robot'] else 1
                    ) + 0.1 * self.scout_data[scout]['assignments']
                    row.append(cost)
                cost_matrix.append(row)

            # Use Hungarian algorithm for optimal assignment
            if cost_matrix and available_scouts:
                from scipy.optimize import linear_sum_assignment
                try:
                    row_ind, col_ind = linear_sum_assignment(cost_matrix)
                    
                    for r, c in zip(row_ind, col_ind):
                        robot = self.robots[r]
                        scout = available_scouts[c]
                        if not self.schedule[match][robot]:
                            self._assign_scout(scout, match, robot)
                except Exception as e:
                    print(f"⚠️ Hungarian algorithm failed for match {match}: {e}")

            # Fill any remaining positions
            remaining = [r for r in self.robots if not self.schedule[match][r]]
            for robot in remaining:
                # Find the best scout for the remaining robot
                best_scout = None
                min_assignments = float('inf')

                # First try available scouts not yet assigned
                candidates = [
                    s for s in available_scouts 
                    if s not in self.schedule[match].values()
                ]
                
                # Fallback to any scout if needed
                if not candidates:
                    candidates = [
                        s for s in self.scout_names
                        if match not in self.unavailability.get(s, [])
                        and s not in self.schedule[match].values()
                    ]

                # Emergency override if still no candidates
                if not candidates:
                    candidates = [
                        s for s in self.scout_names
                        if s not in self.schedule[match].values()
                    ]

                if candidates:
                    # Sort by total assignments and robot consistency
                    candidates.sort(key=lambda x: (
                        self.scout_data[x]['assignments'],
                        x != self.scout_data[x]['primary_robot']
                    ))
                    best_scout = candidates[0]
                    self._assign_scout(best_scout, match, robot)
                else:
                    print(f"🆘 Critical error: No candidates found for match {match} robot {robot}")

    def _assign_scout(self, scout, match, robot):
        self.schedule[match][robot] = scout
        self.scout_data[scout]['assignments'] += 1
        self.scout_data[scout]['assigned_robot'][robot] += 1
        self.scout_data[scout]['last_match'] = match

    def validate_and_visualize(self):
        """Validate the schedule and generate a visualization."""
        # Validation checks
        self._validate_coverage()
        self._warn_constraints()
        
        # Create DataFrame
        schedule_df = pd.DataFrame.from_dict(self.schedule, orient='index')
        
        # Create visualization
        self._create_heatmap(schedule_df)
        return schedule_df

    def _validate_coverage(self):
        """Ensure all matches and robots are covered with detailed errors."""
        errors = []
        for match_num, robots in self.schedule.items():
            missing = [robot for robot, scout in robots.items() if scout is None]
            if missing:
                errors.append(
                    f"❌ Uncovered robots in match {match_num}: {', '.join(missing)}\n"
                    f"    Current assignments: { {k: v for k, v in robots.items() if v} }"
                )
        
        if errors:
            raise AssertionError("\n".join([
                "COVERAGE FAILURE: Missing assignments detected",
                "==============================================",
                *errors,
                f"\nTotal coverage errors: {len(errors)}"
            ]))

    def _warn_constraints(self):
        """Provide detailed warnings about constraint deviations."""
        warnings = []
        for scout in self.scout_names:
            # Get sorted list of worked matches
            worked_matches = sorted(
                [m for m, robots in self.schedule.items() 
                if scout in robots.values()]
            )
            
            if not worked_matches:
                warnings.append(f"⚠️ Scout {scout} has no assignments")
                continue

            # Track consecutive work streaks
            current_streak = 1
            max_streak = 1
            last_match = worked_matches[0]
            
            for match in worked_matches[1:]:
                if match == last_match + 1:
                    current_streak += 1
                    max_streak = max(max_streak, current_streak)
                else:
                    gap = match - last_match - 1
                    if gap < self.target_break:
                        warnings.append(
                            f"⚠️ Short break: {scout} had {gap} match break "
                            f"between {last_match} and {match} (target: {self.target_break})"
                        )
                    current_streak = 1
                last_match = match

            if max_streak > self.target_consecutive:
                warnings.append(
                    f"⚠️ Long streak: {scout} worked {max_streak} consecutive matches "
                    f"(target: {self.target_consecutive})"
                )

            # Check robot consistency
            robot_counts = self.scout_data[scout]['assigned_robot']
            if len(robot_counts) > 1:
                primary = self.scout_data[scout]['primary_robot']
                robot_dist = ", ".join([f"{k} ({v})" for k, v in robot_counts.items()])
                warnings.append(
                    f"⚠️ Robot inconsistency: {scout} (primary: {primary}) "
                    f"assigned to {robot_dist}"
                )

        if warnings:
            print("\n".join([
                "CONSTRAINT WARNINGS:",
                "====================",
                *warnings,
                f"\nTotal warnings: {len(warnings)}"
            ]))

    def _create_heatmap(self, df):
        """Generate a table-based visualization similar to the reference code."""
        plt.figure(figsize=(14, 20))
        
        # Use tab20 colormap
        cmap = plt.colormaps['tab20']
        scout_colors = {scout: cmap(i % 20) 
                    for i, scout in enumerate(self.scout_names)}
        
        # Create cell colors array
        cell_colors = []
        for match in df.index:
            row_colors = []
            for robot in df.columns:
                scout = df.loc[match, robot]
                if pd.notna(scout):
                    row_colors.append(scout_colors[scout])
                else:
                    row_colors.append('white')
            cell_colors.append(row_colors)
        
        # Create table
        fig, ax = plt.subplots(figsize=(14, 20))
        ax.axis('tight')
        ax.axis('off')
        
        # Create the table
        table = ax.table(
            cellText=df.values,
            colLabels=df.columns,
            rowLabels=df.index,
            cellColours=cell_colors,
            cellLoc='center',
            loc='center'
        )
        
        # Adjust table properties
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.2)
        
        # Add title
        plt.title('Scouting Assignment Schedule', fontsize=16, pad=20)
        
        # Create legend
        legend_elements = [
            plt.Rectangle((0,0),1,1, color=scout_colors[scout])
            for scout in self.scout_names
        ]
        plt.legend(
            legend_elements,
            self.scout_names,
            loc='upper center',
            bbox_to_anchor=(0.5, -0.05),
            ncol=4,
            fontsize=10
        )
        
        # Adjust layout and save
        plt.tight_layout()
        plt.savefig(fun+'scouting_schedule.png', bbox_inches='tight', dpi=150)
        plt.close()
        
        print("Schedule visualization saved to 'scouting_schedule.png'")

# Usage
scout_names = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 
               'Frank', 'Grace', 'Hank', 'Ivy', 'Jack']
total_matches = 74
unavailability = {
    'Alice': [1, 2, 3],
    'Bob': [4, 5],
    'Charlie': [10, 11, 12],
}

scheduler = FlexibleScoutScheduler(
    scout_names=scout_names,
    total_matches=total_matches,
    unavailability=unavailability,
    target_consecutive=10,
    target_break=10
)

scheduler.generate_work_schedule()
scheduler.assign_robots()
schedule_df = scheduler.validate_and_visualize()