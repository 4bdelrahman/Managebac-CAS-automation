"""
Generate CAS reflections using Gemini AI.
Learns from past reflections and creates personalized, authentic reflections.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash')


def load_training_data() -> Dict:
    """Load training data from the Resala CAS Project folder."""
    training_path = Path(os.getenv('TRAINING_DATA_PATH', 'Resala CAS Project trainng'))
    text_path = training_path / 'Text training'
    
    training_data = {
        'description': '',
        'reflections': [],
        'learning_outcomes': ''
    }
    
    # Load description
    desc_file = text_path / 'Description and goals.txt'
    if desc_file.exists():
        with open(desc_file, 'r', encoding='utf-8') as f:
            training_data['description'] = f.read()
    
    # Load reflections
    for i in range(1, 10):  # Try reflection 1-9
        ref_file = text_path / f'Reflection {i}.txt'
        ref_file_lower = text_path / f'reflection {i}.txt'
        
        if ref_file.exists():
            with open(ref_file, 'r', encoding='utf-8') as f:
                training_data['reflections'].append(f.read())
        elif ref_file_lower.exists():
            with open(ref_file_lower, 'r', encoding='utf-8') as f:
                training_data['reflections'].append(f.read())
    
    # Load learning outcomes
    lo_file = text_path / 'learning outcomes.txt'
    if lo_file.exists():
        with open(lo_file, 'r', encoding='utf-8') as f:
            training_data['learning_outcomes'] = f.read()
    
    return training_data


def generate_reflection(
    activity_description: str,
    image_analysis: Optional[str] = None,
    learning_outcomes: Optional[List[str]] = None,
    date: Optional[str] = None,
    cas_strand: str = "Service",
    duration_hours: Optional[float] = None
) -> Dict:
    """
    Generate a CAS reflection based on activity details.
    
    Args:
        activity_description: Brief description of what you did
        image_analysis: Optional analysis from analyze_cas_images.py
        learning_outcomes: List of learning outcome numbers (e.g., ["1", "2", "5"])
        date: Date of activity (e.g., "November 20, 2025")
        cas_strand: "Creativity", "Activity", or "Service"
        duration_hours: How many hours spent
        
    Returns:
        Dictionary with generated reflection
    """
    print("🤖 Generating CAS reflection...")
    
    # Load training data
    training_data = load_training_data()
    print(f"📚 Loaded {len(training_data['reflections'])} example reflections")
    
    # Build context from training data
    training_context = f"""
TRAINING DATA - Learn from these examples:

PROJECT DESCRIPTION:
{training_data['description']}

LEARNING OUTCOMES:
{training_data['learning_outcomes']}

EXAMPLE REFLECTIONS (learn the writing style):
"""
    
    for i, reflection in enumerate(training_data['reflections'], 1):
        training_context += f"\n--- Example {i} ---\n{reflection}\n"
    
    # Build the generation prompt
    prompt = f"""{training_context}

---

Now, write a NEW CAS reflection based on this activity:

ACTIVITY DETAILS:
- Description: {activity_description}
- Date: {date or 'Recent'}
- CAS Strand: {cas_strand}
- Duration: {duration_hours or 'N/A'} hours
- Learning Outcomes: {', '.join(learning_outcomes) if learning_outcomes else 'To be determined'}

"""
    
    if image_analysis:
        prompt += f"""
IMAGE ANALYSIS:
{image_analysis}

"""
    
    prompt += """
INSTRUCTIONS:
1. Write in the SAME STYLE as the example reflections above
2. Match the tone, vocabulary level, and structure
3. Be authentic and personal - this should sound like the student who wrote the examples
4. Include specific details from the activity description and image analysis
5. Reference the learning outcomes naturally (e.g., "This showed me LO1..." or "I demonstrated LO5 by...")
6. Keep it concise but meaningful (similar length to the examples)
7. Use a mix of English and Arabic terms where appropriate (like the examples)
8. Focus on personal growth, challenges, and impact

FORMAT:
Reflection [number]: [Title] (LO[X] & LO[Y])
Date: [date]
CAS Strand: [strand]

[Reflection text - 2-3 paragraphs]

Write the reflection now:"""

    try:
        # Generate reflection
        response = model.generate_content(prompt)
        reflection_text = response.text.strip()
        
        print("\n✨ Reflection Generated!")
        print("=" * 60)
        print(reflection_text)
        print("=" * 60)
        
        return {
            "success": True,
            "reflection": reflection_text,
            "activity_description": activity_description,
            "learning_outcomes": learning_outcomes,
            "date": date,
            "cas_strand": cas_strand,
            "duration_hours": duration_hours
        }
        
    except Exception as e:
        print(f"\n❌ Error generating reflection: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def main():
    """Interactive CLI for generating reflections."""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--auto', action='store_true', help='Run in auto mode using generated idea')
    args = parser.parse_args()

    print("=" * 60)
    print("CAS REFLECTION GENERATOR")
    print("=" * 60)
    
    if args.auto:
        print("🤖 Running in AUTO mode...")
        idea_file = Path(".tmp/generated_idea.json")
        if not idea_file.exists():
            print("❌ No generated idea found! Run generate_idea.py first.")
            return
            
        with open(idea_file, 'r', encoding='utf-8') as f:
            idea = json.load(f)
            
        activity_description = idea['description']
        date = idea['date']
        cas_strand = idea['cas_strand']
        duration = str(idea['duration'])
        learning_outcomes = idea['learning_outcomes']
        
        print(f"📝 Using idea: {activity_description}")
        
    else:
        # Get activity details interactively
        print("\n📝 Enter activity details:\n")
        
        activity_description = input("Activity description: ")
        date = input("Date (e.g., November 20, 2025): ")
        cas_strand = input("CAS Strand (Creativity/Activity/Service) [Service]: ") or "Service"
        duration = input("Duration in hours [2]: ") or "2"
        
        print("\nLearning Outcomes:")
        print("1 - Identify strengths and develop areas for growth")
        print("2 - Demonstrate challenges and new skills")
        print("3 - Initiate and plan a CAS experience")
        print("4 - Show commitment and perseverance")
        print("5 - Work collaboratively")
        print("6 - Engage with global significance")
        print("7 - Consider ethics of choices and actions")
        
        lo_input = input("\nEnter learning outcome numbers (comma-separated, e.g., 1,5): ")
        learning_outcomes = [lo.strip() for lo in lo_input.split(',') if lo.strip()]
    
    # Check for image analysis
    image_analysis = None
    analysis_file = Path(".tmp/image_analysis.json")
    if analysis_file.exists():
        if args.auto:
             # In auto mode, use images if available without asking
             use_images = 'y'
        else:
            use_images = input("\n📸 Found image analysis. Use it? (y/n) [y]: ") or "y"
            
        if use_images.lower() == 'y':
            with open(analysis_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data.get('success'):
                    image_analysis = data.get('analysis')
                    print("✓ Using image analysis")
    
    # Generate reflection
    result = generate_reflection(
        activity_description=activity_description,
        image_analysis=image_analysis,
        learning_outcomes=learning_outcomes,
        date=date,
        cas_strand=cas_strand,
        duration_hours=float(duration)
    )
    
    # Save result
    if result.get('success'):
        output_file = ".tmp/generated_reflection.json"
        os.makedirs(".tmp", exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Reflection saved to: {output_file}")
        
        # Also save as text file
        text_file = ".tmp/generated_reflection.txt"
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(result['reflection'])
        print(f"💾 Text version saved to: {text_file}")
    
    return result


if __name__ == "__main__":
    main()
