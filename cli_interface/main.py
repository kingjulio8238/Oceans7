import inquirer
from storage import ModelTeamStorage

def main():
    # Available strategies for AI model analysis
    available_strategies = [
        # these strategies are all up for change
        'Analyst (Data pattern recognition and model behavior analysis)',
        'Reverse Engineer (Architecture and parameter examination)',
        'Prompt Engineer (Input-output relationship testing)',
        'Security Tester (Vulnerability assessment)',
        'Performance Benchmarker (Speed and resource analysis)',
        'Model Distiller (Knowledge extraction specialist)',
        'Documentation Specialist (Training data investigation)'
    ]

    # Podcast tones - keeping original tones
    podcast_tones = [
        'Casual and conversational',
        'Professional and formal',
        'Educational and informative',
        'Humorous and entertaining',
        'Debate-style',
        'Interview format',
        'Storytelling'
    ]

    # Strategy selection question
    strategy_question = [
        inquirer.Checkbox('selected_strategies',
                         message="Select your team's analysis strategies (use spacebar to select)",
                         choices=available_strategies,
                         validate=lambda _, x: len(x) >= 2 and len(x) <= 4,
                         ),
    ]

    # Get strategy selections
    answers = inquirer.prompt(strategy_question)
    selected_strategies = answers['selected_strategies']
    
    print("\nYour selected analysis team:")
    for i, strategy in enumerate(selected_strategies, 1):
        print(f"{i}. {strategy}")

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
    
    print(f"\nSelected podcast tone: {selected_tone}")
    
    # Save the selections without prompt
    storage = ModelTeamStorage()
    team_number = storage.save_team(selected_strategies, selected_tone)
    
    print(f"\nYour selections have been saved as Team #{team_number}")
    print("You can find your saved teams in 'podcast_teams.json'")

if __name__ == "__main__":
    main()