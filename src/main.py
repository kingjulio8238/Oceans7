from coordinator import Oceans7Coordinator
from judge_model import JudgeModel
from config import AGENT_CONFIGS, GEMINI_CONFIG
from model_api import HuggingFaceAPI, GeminiAPI
from commentary_gen import CommentaryGenerator, generate_response
import os

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

        # Initialize commentary generator
        api_key = os.getenv("GOOGLE_API_KEY")
        commentary_gen = CommentaryGenerator(api_key=api_key).create_model()

        # generate commentary
        commentary = generate_response(model=commentary_gen, tone="Casual and conversational")
        print(commentary)

    else:
        print("Mission failed - all agents attempted")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())