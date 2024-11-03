import inquirer
from storage import ModelTeamStorage

def get_user_selections():
    # Available strategies for AI model analysis
    available_strategies = [
        'Scatter',
        'Bait',
        'History',
        'Help',
        'Persuasion',
        'Restorying'
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
    
    # Save strategies first
    storage = ModelTeamStorage()
    strategy_number = storage.save_strategies(selected_strategies)
    print(f"\nYour strategies have been saved as Set #{strategy_number}")

    # Here you can add your operation/processing step
    # ...

    # Then get and save tone selection
    tone_question = [
        inquirer.List('tone',
                     message="Select the tone for your podcast",
                     choices=podcast_tones,
                     ),
    ]

    tone_answer = inquirer.prompt(tone_question)
    selected_tone = tone_answer['tone']
    
    print(f"\nSelected podcast tone: {selected_tone}")
    
    # Save tone selection
    tone_number = storage.save_tone(selected_tone)
    print(f"Your tone has been saved as Selection #{tone_number}")
    print("You can find your saved selections in 'podcast_teams.json'")

    return selected_strategies, selected_tone

if __name__ == "__main__":
    get_user_selections()