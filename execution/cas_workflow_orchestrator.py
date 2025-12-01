"""
CAS Workflow Orchestrator - Main automation script.
Coordinates image analysis, reflection generation, and ManageBac submission.
"""

import os
import sys
from pathlib import Path
from typing import List, Optional
import json

# Add execution directory to path
sys.path.insert(0, str(Path(__file__).parent))

from analyze_cas_images import analyze_images
from generate_reflection import generate_reflection
from submit_to_managebac import ManageBacAutomation


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(title.center(60))
    print("=" * 60 + "\n")


def get_image_files(directory: Optional[str] = None) -> List[str]:
    """
    Get image files from a directory or prompt user.
    
    Args:
        directory: Optional directory path
        
    Returns:
        List of image file paths
    """
    if directory:
        path = Path(directory)
        if path.exists() and path.is_dir():
            extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
            images = [str(f) for f in path.iterdir() if f.suffix.lower() in extensions]
            return images
    
    return []


def run_full_workflow():
    """Run the complete CAS automation workflow."""
    print_header("🚀 CAS AUTOMATION WORKFLOW")
    
    print("This workflow will:")
    print("  1. 📸 Analyze your activity photos")
    print("  2. ✍️  Generate a personalized reflection")
    print("  3. 🌐 Submit to ManageBac (with your review)")
    print()
    
    # Step 1: Get activity information
    print_header("STEP 1: Activity Information")
    
    activity_description = input("📝 Describe your activity: ")
    date = input("📅 Date (e.g., December 1, 2025): ")
    cas_strand = input("🎯 CAS Strand (Creativity/Activity/Service) [Service]: ") or "Service"
    duration = input("⏱️  Duration in hours [2]: ") or "2"
    
    print("\n📚 Learning Outcomes:")
    print("  1 - Identify strengths and develop areas for growth")
    print("  2 - Demonstrate challenges and new skills")
    print("  3 - Initiate and plan a CAS experience")
    print("  4 - Show commitment and perseverance")
    print("  5 - Work collaboratively")
    print("  6 - Engage with global significance")
    print("  7 - Consider ethics of choices and actions")
    
    lo_input = input("\n🎯 Learning outcome numbers (comma-separated, e.g., 1,5): ")
    learning_outcomes = [lo.strip() for lo in lo_input.split(',') if lo.strip()]
    
    # Step 2: Image analysis
    print_header("STEP 2: Image Analysis")
    
    use_images = input("📸 Do you have photos to analyze? (y/n): ")
    image_analysis = None
    
    if use_images.lower() == 'y':
        # Check for training photos directory
        training_photos = Path("Resala CAS Project trainng/Photos training")
        
        if training_photos.exists():
            use_training = input(f"  Use photos from '{training_photos}'? (y/n): ")
            if use_training.lower() == 'y':
                image_files = get_image_files(str(training_photos))
                print(f"  Found {len(image_files)} images")
            else:
                image_dir = input("  Enter directory path with photos: ")
                image_files = get_image_files(image_dir)
        else:
            image_dir = input("  Enter directory path with photos: ")
            image_files = get_image_files(image_dir)
        
        if image_files:
            print(f"\n  Analyzing {len(image_files)} images...")
            result = analyze_images(image_files)
            
            if result.get('success'):
                image_analysis = result.get('analysis')
                print("\n  ✅ Image analysis complete!")
            else:
                print("\n  ⚠️  Image analysis failed, continuing without it")
        else:
            print("  ⚠️  No images found")
    
    # Step 3: Generate reflection
    print_header("STEP 3: Generate Reflection")
    
    print("🤖 Generating your personalized reflection...")
    print("  (This uses your training data to match your writing style)")
    
    reflection_result = generate_reflection(
        activity_description=activity_description,
        image_analysis=image_analysis,
        learning_outcomes=learning_outcomes,
        date=date,
        cas_strand=cas_strand,
        duration_hours=float(duration)
    )
    
    if not reflection_result.get('success'):
        print("\n❌ Reflection generation failed!")
        return
    
    # Step 4: Review and edit
    print_header("STEP 4: Review & Edit")
    
    print("📄 Generated Reflection:")
    print("-" * 60)
    print(reflection_result['reflection'])
    print("-" * 60)
    
    print("\n✏️  Options:")
    print("  1. Submit as-is")
    print("  2. Edit and regenerate")
    print("  3. Save and exit (submit manually later)")
    
    choice = input("\nYour choice (1/2/3): ")
    
    if choice == '2':
        print("\n📝 Please edit the reflection in: .tmp/generated_reflection.txt")
        print("  Then run this script again, or run submit_to_managebac.py directly")
        return
    elif choice == '3':
        print("\n💾 Reflection saved to .tmp/generated_reflection.json")
        print("  Run 'python execution/submit_to_managebac.py' when ready to submit")
        return
    
    # Step 5: Submit to ManageBac
    print_header("STEP 5: Submit to ManageBac")
    
    confirm = input("⚠️  Ready to submit to ManageBac? (yes/no): ")
    if confirm.lower() != 'yes':
        print("\n❌ Submission cancelled")
        print("  Reflection saved to .tmp/generated_reflection.json")
        return
    
    print("\n🌐 Launching ManageBac automation...")
    print("  ⚠️  The browser will open - you may need to:")
    print("     - Complete 2FA if enabled")
    print("     - Navigate to CAS section manually")
    print("     - Review and submit the form")
    
    automation = ManageBacAutomation(headless=False)
    automation.submit_reflection(reflection_result)
    
    print_header("✅ WORKFLOW COMPLETE")
    print("🎉 Your CAS reflection has been processed!")
    print("\n📁 Files created:")
    print("  - .tmp/image_analysis.json (if images were used)")
    print("  - .tmp/generated_reflection.json")
    print("  - .tmp/generated_reflection.txt")
    print("  - .tmp/submission_screenshot.png")


def main():
    """Main entry point."""
    try:
        run_full_workflow()
    except KeyboardInterrupt:
        print("\n\n⚠️  Workflow cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
