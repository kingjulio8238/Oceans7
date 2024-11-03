from flask import Flask, render_template, request, jsonify
import json
import os
import sys

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import config

app = Flask(__name__)

print("Starting Flask application...")

@app.route('/')
def index():
    print("Loading index page...")
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()
        tone = data.get('tone', '')
        info_to_extract = data.get('info_to_extract', '')
        
        print(f"Received data: tone='{tone}', info_to_extract='{info_to_extract}'")
        
        # Update the config module directly
        config.COMMENTARY_CONFIG["tone"] = tone
        config.COMMENTARY_CONFIG["info_to_extract"] = info_to_extract
        
        print(f"Updated COMMENTARY_CONFIG: {config.COMMENTARY_CONFIG}")
            
        return jsonify({"status": "success", "message": "Configuration updated"})
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/check_config')
def check_config():
    return jsonify({
        "tone": config.COMMENTARY_CONFIG["tone"],
        "info_to_extract": config.COMMENTARY_CONFIG["info_to_extract"]
    })

if __name__ == "__main__":
    print("Flask server starting on http://127.0.0.1:5000")
    app.run(debug=True)
