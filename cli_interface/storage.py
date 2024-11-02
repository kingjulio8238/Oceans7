import json
from datetime import datetime

class ModelTeamStorage:
    def __init__(self):
        self.filename = 'podcast_teams.json'
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"strategies_selections": [], "tone_selections": []}
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=2)

    def save_strategies(self, strategies):
        with open(self.filename, 'r') as f:
            data = json.load(f)
        
        strategy_entry = {
            "timestamp": datetime.now().isoformat(),
            "strategies": strategies
        }
        data["strategies_selections"].append(strategy_entry)
        
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        return len(data["strategies_selections"])

    def save_tone(self, tone):
        with open(self.filename, 'r') as f:
            data = json.load(f)
        
        tone_entry = {
            "timestamp": datetime.now().isoformat(),
            "tone": tone
        }
        data["tone_selections"].append(tone_entry)
        
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        return len(data["tone_selections"])