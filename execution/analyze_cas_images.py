"""
Analyze CAS activity images using Gemini Vision API.
Extracts context and details from photos to inform reflection generation.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict
import json
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash')


def analyze_images(image_paths: List[str]) -> Dict:
    """
    Analyze CAS activity images and extract context.
    
    Args:
        image_paths: List of paths to image files
        
    Returns:
        Dictionary containing analysis results
    """
    print(f"📸 Analyzing {len(image_paths)} images...")
    
    # Load images
    images = []
    for path in image_paths:
        try:
            img = Image.open(path)
            images.append(img)
            print(f"  ✓ Loaded: {Path(path).name}")
        except Exception as e:
            print(f"  ✗ Error loading {path}: {e}")
            continue
    
    if not images:
        return {"error": "No images could be loaded"}
    
    # Create analysis prompt
    prompt = """Analyze these CAS (Creativity, Activity, Service) activity photos.

Please provide:
1. **Activity Type**: What activity is shown? (e.g., charity work, sports, art project)
2. **Setting**: Where is this taking place? (indoor/outdoor, specific location if visible)
3. **People**: How many people are involved? What are they doing?
4. **Actions**: What specific tasks or activities are being performed?
5. **Materials/Objects**: What items, equipment, or materials are visible?
6. **Atmosphere**: What's the mood/energy? (collaborative, focused, energetic, etc.)
7. **Key Details**: Any specific details that would be important for a reflection (safety concerns, organization, teamwork, challenges visible, etc.)

Be specific and observational. Focus on concrete details that would help write an authentic reflection."""

    try:
        # Generate analysis
        response = model.generate_content([prompt] + images)
        analysis_text = response.text
        
        print("\n🔍 Analysis Complete!")
        print("=" * 60)
        print(analysis_text)
        print("=" * 60)
        
        return {
            "success": True,
            "analysis": analysis_text,
            "num_images": len(images),
            "image_paths": image_paths
        }
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def main():
    """Main function for command-line usage."""
    if len(sys.argv) < 2:
        print("Usage: python analyze_cas_images.py <image1> <image2> ...")
        print("Example: python analyze_cas_images.py photo1.jpg photo2.jpg")
        sys.exit(1)
    
    image_paths = sys.argv[1:]
    
    # Validate paths
    valid_paths = []
    for path in image_paths:
        if os.path.exists(path):
            valid_paths.append(path)
        else:
            print(f"⚠️  Warning: File not found: {path}")
    
    if not valid_paths:
        print("❌ No valid image files provided")
        sys.exit(1)
    
    # Analyze images
    result = analyze_images(valid_paths)
    
    # Save results
    output_file = ".tmp/image_analysis.json"
    os.makedirs(".tmp", exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    return result


if __name__ == "__main__":
    main()
