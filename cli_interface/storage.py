import json
import os
from datetime import datetime

class ModelTeamStorage:
    def __init__(self):
        self.storage_file = 'podcast_teams.json'

    def save_team(self, models, tone):
        data = {
            'timestamp': datetime.now().isoformat(),
            'models': models,
            'tone': tone
        }
        
        # Load existing teams or create new list
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as f:
                teams = json.load(f)
        else:
            teams = []
            
        # Add new team
        teams.append(data)
        
        # Save back to file
        with open(self.storage_file, 'w') as f:
            json.dump(teams, f, indent=2)
        
        return len(teams)  # Return the team number