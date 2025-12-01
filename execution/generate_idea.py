"""
Generate new CAS activity ideas using Gemini.
Invents plausible next sessions for the project based on training data.
"""

import os
import json
import datetime
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash')

def load_context() -> str:
    """Load project context from training data."""
    training_path = Path(os.getenv('TRAINING_DATA_PATH', 'Resala CAS Project trainng'))
    desc_file = training_path / 'Text training' / 'Description and goals.txt'
    
    if desc_file.exists():
        with open(desc_file, 'r', encoding='utf-8') as f:
            return f.read()
    return "Volunteering at Resala Charity, organizing clothes and helping the community."

def generate_idea() -> dict:
    """Generate a new valid activity idea."""
    print("💡 Generating new activity idea...")
    
    context = load_context()
    today = datetime.datetime.now().strftime("%B %d, %Y")
    
    prompt = f"""
    CONTEXT:
    Student is doing a CAS project:
    {context}
    
    TASK:
    Invent a REALISTIC, SPECIFIC activity for the "next session" of this project.
    It should be something they plausibly did today ({today}).
    
    Examples of activities:
    - Sorting winter clothes for distribution
    - Packing Ramadan food boxes
    - Organizing the warehouse shelves
    - Labeling donation bags
    - Coordinating with new volunteers
    
    REQUIREMENTS:
    1. "description": 1 sentence describing what was done today. Be specific (e.g., "Sorted 50 bags", "Fixed the labeling system").
    2. "duration": Number of hours (between 2 and 4).
    3. "strand": Always "Service".
    4. "learning_outcomes": Select 2-3 relevant outcome numbers (1-7).
    
    OUTPUT JSON ONLY:
    {{
        "description": "...",
        "date": "{today}",
        "duration": 3,
        "cas_strand": "Service",
        "learning_outcomes": ["1", "4"]
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Clean up json block if present
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
            
        data = json.loads(text)
        
        # Save to file
        output_file = Path(".tmp/generated_idea.json")
        os.makedirs(".tmp", exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
        print(f"✅ Idea generated: {data['description']}")
        return data
        
    except Exception as e:
        print(f"❌ Error generating idea: {e}")
        return None

if __name__ == "__main__":
    generate_idea()
