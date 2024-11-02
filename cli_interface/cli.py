import inquirer
from storage import ModelTeamStorage

def main():
    # Available models
    available_models = [
        'GPT-4',
        'Claude 2',
        'LLaMA 2',
        'Mistral',
        'PaLM',
        'BLOOM',
    ]

    # Podcast tones
    podcast_tones = [
        'Casual and conversational',
        'Professional and formal',
        'Educational and informative',
        'Humorous and entertaining',
        'Debate-style',
        'Interview format',
        'Storytelling'
    ]

    # Model selection question
    models_question = [
        inquirer.Checkbox('selected_models',
                         message="Select the AI models for your podcast team (use spacebar to select)",
                         choices=available_models,
                         validate=lambda _, x: len(x) >= 2 and len(x) <= 4,
                         ),
    ]

    # Get model selections
    answers = inquirer.prompt(models_question)
    selected_models = answers['selected_models']
    
    print("\nYour selected team of models:")
    for i, model in enumerate(selected_models, 1):
        print(f"{i}. {model}")

    # Tone selection question
    tone_question = [
        inquirer.List('tone',
                     message="Select the tone for your podcast",
                     choices=podcast_tones,
                     ),
    ]

    # Get tone selection
    tone_answer = inquirer.prompt(tone_question)
    selected_tone = tone_answer['tone']
    
    # Save the selections
    storage = ModelTeamStorage()
    team_number = storage.save_team(selected_models, selected_tone)
    
    print(f"\nSelected podcast tone: {selected_tone}")
    print(f"\nYour selections have been saved as Team #{team_number}")
    print("You can find your saved teams in 'podcast_teams.json'")

if __name__ == "__main__":
    main()