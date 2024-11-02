import google.generativeai as genai
import json
import argparse

def load_json_lines(file_path):
    """
    Reads a file containing multiple JSON objects (one per line) and returns a list of dictionaries.
    
    :param file_path: Path to the text file.
    :return: List of dictionaries parsed from the JSON objects.
    """
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if line:  # Ensure the line is not empty
                try:
                    json_object = json.loads(line)
                    data.append(json_object)
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON on line {line_number}: {e}")
    return data

def generate_prompt(history_logs:list, tone:str) -> None:
    prompt = f"""
    You are a commentator for a llm wresling match where small language models
    are attacking a larger language model using adversarial prompts.
    You are receiving history logs of the attacks and the tone of the commentary.
    history_logs = {history_logs}, tone = {tone};
    The history logs is a list containing the following information 
    per attacker model's attacks:
    - timestamp
    - target_info
    - success
    - agent_data (information about the attacking model)
        - prompt
        - strategy
        - response (response from the larger model)
        - analysis
            - defensive_indicators
            - financial_openness
            - trust_indicators
            - suggested_approach
            - revealed_info
    Your task is to generate a commentary script based on the history logs and the specified tone.
    Do not read the timestamps, but use them as references for the order of the attacks.
    """
    
    return prompt


def generate_response(model: str, prompt: str, 
                      temp: float, top_p: float, top_k: int) -> None:
    # get api key for Google AI studio
    with open('api.json') as f:
        data = json.load(f)
        api_key = data['api_key']

    generation_config = {
    "temperature": temp,
    "top_p": top_p,
    "top_k": top_k,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }
    
    # create a model
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name=model,
        generation_config=generation_config)
    
    # generate a response
    response = model.generate_content(prompt)
    print(response.text)

if __name__ == '__main__':
    # argument parser for model
    parser = argparse.ArgumentParser()
    parser.add_argument('-model', type=str, default='gemini-1.5-flash', help='e.g., gemini-1.5-pro-002')
    parser.add_argument('--temp', type=float, default=1)
    parser.add_argument('--top_p', type=float, default=0.95)
    parser.add_argument('--top_k', type=int, default=40)
    args = parser.parse_args()

    prompt = generate_prompt()
    generate_response(args.model, prompt, args.temp, args.top_p, args.top_k)
