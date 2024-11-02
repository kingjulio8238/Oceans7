from coordinator import Oceans7Coordinator
from judge_model import JudgeModel
from config import AGENT_CONFIGS, GEMINI_CONFIG
from model_api import HuggingFaceAPI, GeminiAPI

async def main():
    # Initialize APIs
    hf_api = HuggingFaceAPI()
    gemini_api = GeminiAPI(config=GEMINI_CONFIG)
    
    # Initialize agents
    agents = []
    team_plan = {}
    
    for config in AGENT_CONFIGS:
        agent = config['class'](
            prompt=config['prompt'],
            team_plan=team_plan,
            hf_api=hf_api,
            gemini_api=gemini_api,
            model=config['model']
        )
        agents.append(agent)
    
    # Initialize judge
    judge = JudgeModel()
    
    # Initialize coordinator
    coordinator = Oceans7Coordinator(agents, judge)
    
    # Execute mission
    success = await coordinator.execute_mission()
    
    if success:
        print("Mission completed successfully")
    else:
        print("Mission failed - all agents attempted")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 