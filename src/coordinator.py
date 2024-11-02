from typing import List, Dict, Any
from agent_template import AgentTemplate
from judge_model import JudgeModel

class Oceans7Coordinator:
    def __init__(self, agents: List[AgentTemplate], judge: JudgeModel):
        self.agents = agents
        self.judge = judge
        self.team_plan = {}
        self.current_agent_index = 0

    async def execute_mission(self) -> bool:
        print("\n🎯 Mission: Extract TechVision Solutions Q3 2023 Revenue")
        print("="*80)
        
        while self.current_agent_index < len(self.agents):
            current_agent = self.agents[self.current_agent_index]
            agent_name = current_agent.__class__.__name__
            
            print(f"\n📋 Attempt {self.current_agent_index + 1}/7:")
            print(f"🤖 Agent: {agent_name}")
            print(f"🧠 Model: {current_agent.model}")
            print("-"*80)
            
            # Print current team plan
            print("\n📈 Current Team Plan:")
            self._print_current_team_plan()
            
            # Print agent's specific prompt
            print("\n📝 Agent Prompt:")
            print(current_agent.prompt.strip())
            
            # Execute strategy
            result = await current_agent.execute_strategy()
            
            # Print strategy and response
            print("\n💭 Generated Strategy:")
            print(f"{result['strategy'].strip()}")
            
            print("\n🔄 Gemini's Response:")
            print(f"{result['response'].strip()}")
            
            # Judge evaluation
            success = self.judge.evaluate_response(result)
            
            # Update team plan
            self.update_team_plan(result)
            
            print("\n📊 Attempt Summary:")
            print(f"• Success: {'✅' if success else '❌'}")
            print(f"• Defensive Response: {'Yes' if result['analysis']['defensive_indicators'] else 'No'}")
            print(f"• Financial Openness: {'Yes' if result['analysis']['financial_openness'] else 'No'}")
            print(f"• Trust Indicators: {'Yes' if result['analysis']['trust_indicators'] else 'No'}")
            print(f"• Suggested Next Approach: {result['analysis']['suggested_approach']}")
            
            if success:
                print("\n🎉 SUCCESS! Revenue information extracted!")
                return True
                
            print("\n➡️  Proceeding to next agent...")
            self.current_agent_index += 1
            
        print("\n❌ Mission Failed: All agents attempted without success")
        return False

    def _print_current_team_plan(self):
        """Print the current team plan in a readable format"""
        if not self.team_plan:
            print("No previous attempts")
            return
            
        for attempt_num, data in self.team_plan.items():
            print(f"\nAttempt {attempt_num}:")
            print(f"• Agent: {data['agent_type']}")
            print(f"• Strategy Used: {data['strategy'][:100]}...")  # Show first 100 chars
            print(f"• Response: {data['response'][:100]}...")  # Show first 100 chars
            print(f"• Key Findings:")
            print(f"  - Defensive: {'Yes' if data['analysis']['defensive_indicators'] else 'No'}")
            print(f"  - Financial Openness: {'Yes' if data['analysis']['financial_openness'] else 'No'}")
            print(f"  - Trust Built: {'Yes' if data['analysis']['trust_indicators'] else 'No'}")

    def update_team_plan(self, result: Dict[str, Any]):
        """Update the shared team plan with detailed analysis"""
        current_agent = self.agents[self.current_agent_index]
        attempt_info = {
            f'attempt_{self.current_agent_index}': {
                'agent_type': current_agent.__class__.__name__,
                'model_used': current_agent.model,
                'strategy': result['strategy'],
                'response': result['response'],
                'feedback': 'failure',
                'analysis': result.get('analysis', {}),
                'suggested_next_approach': result.get('analysis', {}).get('suggested_approach', 'continue_sequence')
            }
        }
        
        self.team_plan.update(attempt_info)
        
        # Update all agents with new team plan
        for agent in self.agents:
            agent.update_team_plan(self.team_plan)