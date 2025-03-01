from typing import Dict, List, Set, Tuple
import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict, Counter

class ScoutScheduler:
    """
    A scheduler for assigning scouts to monitor players/teams across a season.
    Uses a sliding window approach to optimize scout assignments across multiple matches.
    """
    
    def __init__(
        self,
        scout_names: List[str],
        total_matches: int,
        unavailability: Dict[str, List[int]],
        breaks: List[int],
        teams_to_scout: List[str] = None,
        target_consecutive_matches: int = 10,
        target_rest_matches: int = 10
    ):
        """
        Initialize the scout scheduler with required parameters.
        
        Args:
            scout_names: List of available scouts
            total_matches: Total number of matches in the season
            unavailability: Dictionary mapping scout names to match numbers they cannot attend
            breaks: List of matches after which there are scheduled breaks
            teams_to_scout: List of teams/players requiring scouting (default: R1, R2, R3, B1, B2, B3)
            target_consecutive_matches: Target number of consecutive matches for a scout
            target_rest_matches: Target number of rest matches between scouting periods
        """
        self.scout_names = scout_names
        self.total_matches = total_matches
        self.unavailability = unavailability
        self.breaks = breaks
        self.teams_to_scout = teams_to_scout or ["R1", "R2", "R3", "B1", "B2", "B3"]
        self.target_consecutive_matches = target_consecutive_matches
        self.target_rest_matches = target_rest_matches
        
        # Initialize schedule as a nested dictionary
        self.schedule = {match: {team: None for team in self.teams_to_scout} for match in range(1, total_matches + 1)}
        
        # Track assignments for each scout
        self.scout_assignments = {name: [] for name in scout_names}
        
        # Track consecutive matches worked for each scout
        self.consecutive_matches = {name: 0 for name in scout_names}
        
        # Track matches since last worked for each scout
        self.matches_since_worked = {name: 0 for name in scout_names}
        
        # Track team familiarity (which teams each scout has worked with)
        self.team_familiarity = {name: set() for name in scout_names}
        
        # Segment bounds (determined by scheduled breaks)
        self.segments = self._determine_segments()
        
        # Assignments per match - track how many teams each scout is monitoring each match
        self.match_assignments = {match: {name: 0 for name in scout_names} for match in range(1, total_matches + 1)}

    def _determine_segments(self) -> List[Tuple[int, int]]:
        """
        Determine the schedule segments based on scheduled breaks.
        
        Returns:
            List of tuples (start_match, end_match) for each segment
        """
        segments = []
        start_match = 1
        
        for break_match in self.breaks:
            segments.append((start_match, break_match))
            start_match = break_match + 1
            
        # Add the final segment
        segments.append((start_match, self.total_matches))
        
        return segments
    
    def is_available(self, scout: str, match: int) -> bool:
        """
        Check if a scout is available for a given match.
        
        Args:
            scout: The name of the scout
            match: The match number to check
            
        Returns:
            True if the scout is available, False otherwise
        """
        return match not in self.unavailability.get(scout, [])
    
    def get_available_scouts(self, match: int) -> List[str]:
        """
        Get all scouts available for a specific match.
        
        Args:
            match: The match number to check
            
        Returns:
            List of available scouts
        """
        return [name for name in self.scout_names if self.is_available(name, match)]
    
    def should_rest(self, scout: str) -> bool:
        """
        Determine if a scout should rest based on consecutive matches worked.
        
        Args:
            scout: The name of the scout
            
        Returns:
            True if the scout should rest, False otherwise
        """
        return self.consecutive_matches[scout] >= self.target_consecutive_matches
    
    def select_scout_for_team(self, match: int, team: str, available_scouts: List[str]) -> str:
        """
        Select the best scout for a team on a given match.
        
        Args:
            match: The current match
            team: The team needing scouting
            available_scouts: List of available scouts
            
        Returns:
            Name of selected scout
        """
        # Filter out scouts who should rest unless necessary
        rested_scouts = [s for s in available_scouts if not self.should_rest(s)]
        
        # If no rested scouts are available, use all available scouts
        candidates = rested_scouts if rested_scouts else available_scouts
        
        # First priority: scouts familiar with this team
        familiar_candidates = [s for s in candidates if team in self.team_familiarity[s]]
        if familiar_candidates:
            # Among familiar candidates, prefer those with fewer assignments on this match
            return min(familiar_candidates, key=lambda s: self.match_assignments[match][s])
        
        # Second priority: scouts with the fewest current team assignments overall
        return min(candidates, key=lambda s: len(self.team_familiarity[s]))
    
    def update_tracking(self, match: int, team: str, scout: str) -> None:
        """
        Update tracking information after assigning a scout.
        
        Args:
            match: The current match
            team: The assigned team
            scout: The assigned scout
        """
        # Update schedule
        self.schedule[match][team] = scout
        
        # Update scout assignments
        self.scout_assignments[scout].append((match, team))
        
        # Update match assignments count
        self.match_assignments[match][scout] += 1
        
        # Update team familiarity
        self.team_familiarity[scout].add(team)
        
        # Update consecutive matches worked
        self.consecutive_matches[scout] += 1
        
        # Reset matches since worked
        self.matches_since_worked[scout] = 0
        
        # For all other scouts, increment matches since worked
        for other_scout in self.scout_names:
            if other_scout != scout and match not in self.unavailability.get(other_scout, []):
                if self.match_assignments[match][other_scout] == 0:  # Only increment if not working today
                    self.matches_since_worked[other_scout] += 1
    
    def reset_after_break(self) -> None:
        """Reset consecutive matches worked after a scheduled break."""
        self.consecutive_matches = {name: 0 for name in self.scout_names}
    
    def generate_schedule(self) -> None:
        """Generate the complete schedule using a sliding window approach."""
        # Process each segment
        for segment_start, segment_end in self.segments:
            # Process each match in the segment
            for match in range(segment_start, segment_end + 1):
                # Get available scouts for this match
                available_scouts = self.get_available_scouts(match)
                
                # Ensure we have enough scouts
                if len(available_scouts) < len(self.teams_to_scout):
                    raise ValueError(f"Not enough scouts available for match {match}")
                
                # Assign scouts to teams
                for team in self.teams_to_scout:
                    # Skip if already assigned (shouldn't happen in initial generation)
                    if self.schedule[match][team] is not None:
                        continue
                    
                    # Select scout for this team
                    selected_scout = self.select_scout_for_team(match, team, available_scouts)
                    
                    # Update tracking
                    self.update_tracking(match, team, selected_scout)
                    
                    # Remove from available if fully assigned for this match
                    if self.match_assignments[match][selected_scout] >= 1:  # Adjust if multiple assignments per match are allowed
                        available_scouts = [s for s in available_scouts if s != selected_scout]
            
            # Reset consecutive matches worked after a break
            if segment_end in self.breaks:
                self.reset_after_break()
    
    def optimize_schedule(self, iterations: int = 100) -> None:
        """
        Optimize the schedule by swapping assignments to improve team familiarity.
        
        Args:
            iterations: Number of optimization iterations
        """
        for _ in range(iterations):
            # Randomly select a match
            match = random.randint(1, self.total_matches)
            
            # Randomly select two teams
            team1, team2 = random.sample(self.teams_to_scout, 2)
            
            # Get current assignments
            scout1 = self.schedule[match][team1]
            scout2 = self.schedule[match][team2]
            
            # Skip if either scout is unavailable for the other's team
            if not scout1 or not scout2:
                continue
                
            if not self.is_available(scout1, match) or not self.is_available(scout2, match):
                continue
            
            # Calculate current familiarity score
            current_score = (
                (1 if team1 in self.team_familiarity[scout1] else 0) +
                (1 if team2 in self.team_familiarity[scout2] else 0)
            )
            
            # Calculate new familiarity score if swapped
            new_score = (
                (1 if team2 in self.team_familiarity[scout1] else 0) +
                (1 if team1 in self.team_familiarity[scout2] else 0)
            )
            
            # Swap if it improves the score
            if new_score > current_score:
                # Update the schedule
                self.schedule[match][team1] = scout2
                self.schedule[match][team2] = scout1
                
                # Update assignments
                self.scout_assignments[scout1] = [(m, t if t != team1 else team2) 
                                               for m, t in self.scout_assignments[scout1]]
                self.scout_assignments[scout2] = [(m, t if t != team2 else team1) 
                                               for m, t in self.scout_assignments[scout2]]
    
    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert schedule to a pandas DataFrame.
        
        Returns:
            DataFrame representation of the schedule
        """
        data = []
        for match in range(1, self.total_matches + 1):
            row = {'Match': match}
            for team in self.teams_to_scout:
                row[team] = self.schedule[match][team]
            data.append(row)
        
        return pd.DataFrame(data)
    
    def visualize_schedule(self, filename: str = "/Users/matthewahn/Desktop/"+"scout_schedule.png") -> None:
        """
        Visualize the schedule as a colorful heatmap.
        
        Args:
            filename: Output file name for the visualization
        """
        df = self.to_dataframe()
        
        # Assign a unique color index to each scout
        unique_scouts = list(set(self.scout_names))
        scout_to_index = {name: i for i, name in enumerate(unique_scouts)}
        
        # Create a numerical representation of the schedule for visualization
        numerical_data = np.zeros((self.total_matches, len(self.teams_to_scout)))
        for i in range(self.total_matches):
            for j, team in enumerate(self.teams_to_scout):
                scout = df.iloc[i][team]
                numerical_data[i, j] = scout_to_index.get(scout, -1)
        
        # Prepare the plot
        fig, ax = plt.subplots(figsize=(12, 20))
        
        # Create the heatmap
        cmap = plt.cm.get_cmap('tab20', len(unique_scouts))
        im = ax.imshow(numerical_data, cmap=cmap, aspect='auto')
        
        # Add break markers
        for break_match in self.breaks:
            ax.axhline(y=break_match - 0.5, color='red', linestyle='-', linewidth=2, alpha=0.7)
            ax.text(-0.5, break_match, f"Break", color='red', fontsize=10, ha='right', va='center')
        
        # Set labels
        ax.set_xticks(np.arange(len(self.teams_to_scout)))
        ax.set_xticklabels(self.teams_to_scout)
        ax.set_yticks(np.arange(self.total_matches))
        ax.set_yticklabels(np.arange(1, self.total_matches + 1))
        
        # Add a title
        ax.set_title("Scout Assignment Schedule")
        
        # Add a legend
        handles = [plt.Rectangle((0,0),1,1, color=cmap(scout_to_index[name])) for name in unique_scouts]
        plt.legend(handles, unique_scouts, loc='upper left', bbox_to_anchor=(1, 1))
        
        # Add grid lines
        ax.set_xticks(np.arange(-.5, len(self.teams_to_scout), 1), minor=True)
        ax.set_yticks(np.arange(-.5, self.total_matches, 1), minor=True)
        ax.grid(which='minor', color='black', linestyle='-', linewidth=0.5, alpha=0.2)
        
        # Adjust layout
        plt.tight_layout()
        
        # Save the figure
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
    def analyze_schedule(self) -> Dict:
        """
        Analyze the generated schedule for various metrics.
        
        Returns:
            Dictionary of schedule analysis metrics
        """
        df = self.to_dataframe()
        
        # Count assignments per scout
        assignment_counts = {}
        for scout in self.scout_names:
            count = 0
            for match in range(1, self.total_matches + 1):
                for team in self.teams_to_scout:
                    if df.loc[df['Match'] == match, team].values[0] == scout:
                        count += 1
            assignment_counts[scout] = count
        
        # Calculate work streak lengths
        work_streaks = {}
        for scout in self.scout_names:
            streaks = []
            current_streak = 0
            for match in range(1, self.total_matches + 1):
                # Check if scout is working on this match
                is_working = False
                for team in self.teams_to_scout:
                    if df.loc[df['Match'] == match, team].values[0] == scout:
                        is_working = True
                        break
                
                if is_working:
                    current_streak += 1
                elif current_streak > 0:
                    streaks.append(current_streak)
                    current_streak = 0
            
            # Add the final streak if there is one
            if current_streak > 0:
                streaks.append(current_streak)
            
            work_streaks[scout] = streaks
        
        # Calculate team familiarity
        team_assignments = {}
        for scout in self.scout_names:
            team_counts = {team: 0 for team in self.teams_to_scout}
            for match in range(1, self.total_matches + 1):
                for team in self.teams_to_scout:
                    if df.loc[df['Match'] == match, team].values[0] == scout:
                        team_counts[team] += 1
            team_assignments[scout] = team_counts
        
        return {
            'assignment_counts': assignment_counts,
            'work_streaks': work_streaks,
            'team_assignments': team_assignments
        }

# Example usage
def run_scout_scheduling():
    """Main function to run the scout assignment algorithm."""
    # Input data
    scout_names = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 
                   'Grace', 'Hank', 'Ivy', 'Jack', 'Katie', 'Leo',
                   'Maya', 'Noah', 'Olivia']
    total_matches = 74
    unavailability = {
        'Alice': [1, 2, 3],
        'Bob': [4, 5],
        'Charlie': [10, 11, 12],
        'David': [20, 21],
        'Eve': [30, 31, 32],
        'Frank': [40, 41],
        'Grace': [50, 51, 52],
        'Hank': [60, 61],
        'Ivy': [15, 16, 17],
        'Jack': [25, 26, 27],
        'Katie': [35, 36],
        'Leo': [45, 46, 47],
        'Maya': [55, 56],
        'Noah': [65, 66, 67],
        'Olivia': [5, 6, 7]
    }
    breaks = [22, 55]
    
    # Create scheduler
    scheduler = ScoutScheduler(
        scout_names=scout_names,
        total_matches=total_matches,
        unavailability=unavailability,
        breaks=breaks,
        target_consecutive_matches=10,
        target_rest_matches=10
    )
    
    # Generate and optimize schedule
    scheduler.generate_schedule()
    scheduler.optimize_schedule(iterations=500)
    
    # Visualize the schedule
    scheduler.visualize_schedule(filename="scout_schedule.png")
    
    # Convert to dataframe
    schedule_df = scheduler.to_dataframe()
    
    # Analyze the schedule
    analysis = scheduler.analyze_schedule()
    
    # Print summary
    print("Scout Assignment Schedule Generated!")
    print(f"Total matches: {total_matches}")
    print(f"Total scouts: {len(scout_names)}")
    print(f"Teams scouted: {scheduler.teams_to_scout}")
    
    print("\nAssignment distribution:")
    for scout, count in sorted(analysis['assignment_counts'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {scout}: {count} assignments")
    
    print("\nLongest work streaks:")
    for scout, streaks in analysis['work_streaks'].items():
        if streaks:
            print(f"  {scout}: {max(streaks)} matches")
        else:
            print(f"  {scout}: 0 matches")
    
    print("\nTeam familiarity (top assignments):")
    for scout, assignments in analysis['team_assignments'].items():
        top_team = max(assignments.items(), key=lambda x: x[1])
        print(f"  {scout}: {top_team[0]} ({top_team[1]} matches)")
    
    return schedule_df

if __name__ == "__main__":
    schedule = run_scout_scheduling()
    print("\nFirst 10 matches of schedule:")
    print(schedule.head(10))
    
    # Save to CSV
    schedule.to_csv("scout_schedule.csv", index=False)
    print("\nFull schedule saved to scout_schedule.csv")
    print("Visualization saved to scout_schedule.png")