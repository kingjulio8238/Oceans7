import google.generativeai as genai
import json

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

class CommentaryGenerator:
    def __init__(self, api_key: str):
        self.model = "gemini-1.5-pro-002"
        self.api_key = api_key
        self.temp = 1
        self.top_p = 0.95
        self.top_k = 40

    def create_model(self):
        generation_config = {
        "temperature": self.temp,
        "top_p": self.top_p,
        "top_k": self.top_k,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
        }
        
        # create a model
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(
            model_name=self.model,
            generation_config=generation_config)
        
        return model

def generate_response(model: str,
                      tone: str, log_file: str = "decision_log.txt") -> None:

    history_logs = load_json_lines(log_file)
    prompt = generate_prompt(history_logs, tone)

    # generate a response
    response = model.generate_content(prompt)
    return response.text
