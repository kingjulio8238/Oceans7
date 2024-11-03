from coordinator import Oceans7Coordinator
from judge_model import JudgeModel
from config import AGENT_CONFIGS, GEMINI_CONFIG, GROQ_CONFIG
from model_api import HuggingFaceAPI, GeminiAPI, GroqAPI
from commentary_gen import CommentaryGenerator, generate_response
import os
import logging
import asyncio
import json

async def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Oceans7 Mission...")
    
    # Initialize APIs
    try:
        hf_api = HuggingFaceAPI()
        gemini_api = GeminiAPI(config=GEMINI_CONFIG)
        groq_api = GroqAPI(config=GROQ_CONFIG)
        
        # Pre-load all models
        logger.info("Pre-loading HuggingFace models...")
        for config in AGENT_CONFIGS:
            model_name = config['model']
            logger.info(f"Loading model: {model_name}")
            await hf_api.load_model(model_name)
        
        # Initialize agents
        agents = []
        team_plan = {}
        
        for config in AGENT_CONFIGS:
            agent = config['class'](
                prompt=config['prompt'],
                team_plan=team_plan,
                hf_api=hf_api,
                gemini_api=gemini_api,
                groq_api=groq_api,
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
        else:
            print("Mission failed - all agents attempted")
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

        

        logger.info("Cleaning up resources...")
        hf_api.cleanup()
    except Exception as e:
        logger.error(f"Error during mission execution: {str(e)}")
        raise


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nMission aborted by user")
    except Exception as e:
        print(f"Mission failed with error: {str(e)}")