import google.generativeai as genai
import json
import argparse

def generate_prompt() -> None:
    # get the prompt
    with open('prompts.json') as f:
        data = json.load(f)
        prompt = data['prompt']
    
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
