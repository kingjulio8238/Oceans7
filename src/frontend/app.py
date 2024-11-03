from flask import Flask, render_template, request, jsonify
import json
import os
import sys
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import config

app = Flask(__name__)

logger.info("Starting Flask application...")

@app.route('/')
def index():
    logger.info("Loading index page...")
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()
        tone = data.get('tone', '')
        info_to_extract = data.get('info_to_extract', '')
        
        logger.info(f"Received data: tone='{tone}', info_to_extract='{info_to_extract}'")
        
        if not tone or not info_to_extract:
            raise ValueError("Both tone and info_to_extract are required")
        
        # Update and verify in one step
        config.update_commentary_config(tone, info_to_extract)
        current_config = config.get_commentary_config()
        
        return jsonify({
            "status": "success",
            "message": "Configuration updated",
            "current_config": current_config,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error in submit: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    logger.info("Server starting on http://127.0.0.1:5000")
    app.run(debug=True)
