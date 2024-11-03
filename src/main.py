from coordinator import Oceans7Coordinator
from judge_model import JudgeModel
from config import AGENT_CONFIGS, GEMINI_CONFIG
from model_api import HuggingFaceAPI, GeminiAPI
from commentary_gen import CommentaryGenerator, generate_response
import os
import json

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

        # New changes –– test this by running python cli_interface/main.py and select any strategy except Casual and conversational
        # Get tone directly from JSON file
        with open('cli_interface/podcast_teams.json', 'r') as f:
            data = json.load(f)
            tone_selections = data.get("tone_selections", [])
            current_tone = tone_selections[-1]["tone"] if tone_selections else "Casual and conversational"
        
        # This test case should pass assuming you changed the tone selection in the CLI to something thats not Casual and conversational
        assert current_tone != "Casual and conversational", "ERROR: Tone should not be Casual and conversational"
        commentary = generate_response(model=commentary_gen, tone=current_tone)
        print(commentary)

    else:
        print("Mission failed - all agents attempted")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())