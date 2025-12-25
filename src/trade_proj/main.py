import os
import signal
from datetime import datetime
import sys
from dotenv import load_dotenv
from pathlib import Path

# Windows + Python 3.13: add missing POSIX signals before importing crewai
for missing_sig in ("SIGHUP", "SIGCONT", "SIGTSTP"):
    if not hasattr(signal, missing_sig):
        setattr(signal, missing_sig, signal.SIGTERM)

# Load environment variables
env_path = Path(__file__).resolve()
while env_path.name != "projects":
    env_path = env_path.parent
load_dotenv(env_path / ".env", override=True)

# Import your crew after signal patching and dotenv
from trade_proj.crew import Leads  # Matches your crew.py class name and folder

# Ensure we have somewhere to write any task outputs
os.makedirs("output", exist_ok=True)

def run():
    """Run the Leads crew for client research and email generation."""
    inputs = {
        "current_year": datetime.now().year,
    }

    result = Leads().crew().kickoff(inputs=inputs)
    print(result.raw)

if __name__ == "__main__":
    run()
from flask import Flask, request, jsonify
from trade_proj.crew import Leads

app = Flask(__name__)

@app.route('/analyze_lead', methods=['POST'])
def analyze_lead():
    data = request.json
    result = Leads().crew().kickoff(inputs=data)
    return jsonify(result.json_dict)

if __name__ == '__main__':
    app.run(port=5000)
