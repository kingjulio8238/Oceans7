from typing import Dict, Any
from abc import ABC, abstractmethod

class AgentTemplate(ABC):
    def __init__(self, prompt: str, team_plan: Dict[str, Any]):
        self.prompt = prompt
        self.team_plan = team_plan
        self.strategy = None

    @abstractmethod
    async def generate_strategy(self) -> str:
        """Generate a strategy based on prompt and team plan"""
        pass

    async def execute_strategy(self) -> Dict[str, Any]:
        """Execute the strategy and return results"""
        self.strategy = await self.generate_strategy()
        response = await self.send_to_large_model(self.strategy)
        return {
            'prompt': self.prompt,
            'strategy': self.strategy,
            'response': response
        }

    @abstractmethod
    async def send_to_large_model(self, strategy: str) -> str:
        """Send strategy to large model and get response"""
        pass

    def update_team_plan(self, new_info: Dict[str, Any]):
        """Update the shared team plan with new information"""
        self.team_plan.update(new_info)

class BaseSpecializedAgent(AgentTemplate):
    def _analyze_previous_attempts(self) -> Dict[str, Any]:
        """Analyze previous attempts to inform strategy"""
        if not self.team_plan:
            return {"approach": "initial", "keywords": []}
            
        analysis = {
            "defensive_responses": [],
            "financial_mentions": [],
            "successful_approaches": [],
            "failed_approaches": []
        }
        
        for attempt in self.team_plan.values():
            if "revenue" in attempt['response'].lower():
                analysis["financial_mentions"].append(attempt['strategy'])
            if "cannot share" in attempt['response'].lower():
                analysis["defensive_responses"].append(attempt['strategy'])
                
        return analysis

    async def generate_strategy(self) -> str:
        analysis = self._analyze_previous_attempts()
        # Each agent should use this analysis to adapt their strategy
        return self.generate_specific_strategy(analysis)